# image_service/views.py
import base64
import json
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import AssessmentResult

@csrf_exempt
@require_POST
def submit_assessment(request):
    """
    Combined endpoint that:
      1. Processes the image by sending it to the external image processing service.
      2. Retrieves student answers and details.
      3. Calls the test microservice to get correct answers (as lists) and point weights.
      4. Compares student answers with correct answers while handling:
            - Extra answers or missing answers.
            - Both single-answer and multiple-answer questions.
      5. Computes the total score.
      6. Saves and returns the assessment result.
    """
    # Step 1: Get the image from the request.
    image_data = request.FILES.get('image')
    if not image_data:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    # Prepare the payload for the external image processing service.
    files = {'image': (image_data.name, image_data.read(), image_data.content_type)}
    image_service_url = 'http://127.0.0.1:5000/process_image'  # Adjust as needed
    
    try:
        external_response = requests.post(image_service_url, files=files)
    except Exception as e:
        return JsonResponse({'error': f'Failed to process image: {str(e)}'}, status=500)
    
    if external_response.status_code != 200:
        return JsonResponse({'error': 'Image processing failed',
                             'details': external_response.text},
                            status=external_response.status_code)
    
    try:
        data = external_response.json()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid response from image processing service'}, status=500)
    
    # Step 2: Extract required fields from the external service response.
    assessment_id = data.get("assessmentID")
    student_id = data.get("studentID")
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    variant = data.get("variant")
    student_answers = data.get("answers")  # Expected to be a dict: { "1": ["C"], "2": ["A", "D"], ... }
    student_sheet_b64 = data.get("student_sheet")
    
    if not all([assessment_id, student_id, first_name, last_name, variant, student_answers, student_sheet_b64]):
        return JsonResponse({'error': 'Missing required fields in image processing response'}, status=400)
    
    # Step 3: Retrieve correct answers and point weights from the test microservice.
    test_service_url = f'http://127.0.0.1:8001/api/tests/{assessment_id}/correct_answers/'
    test_response = requests.get(test_service_url)
    if test_response.status_code != 200:
        return JsonResponse({'error': 'Failed to retrieve correct answers from test microservice'},
                            status=test_response.status_code)
    
    test_data = test_response.json()
    correct_answers = test_data.get("correct_answers")  # Each value is expected to be a list.
    points_mapping = test_data.get("points")
    
    if correct_answers is None or points_mapping is None:
        return JsonResponse({'error': 'Test microservice did not return proper data.'}, status=500)
    
    # Step 4: Compute total score.
    # We iterate over the expected questions from correct_answers.
    total_score = 0.0
    for question_num, correct_ans_list in correct_answers.items():
        # Ensure correct_ans_list is a list.
        if not isinstance(correct_ans_list, list):
            correct_ans_list = [correct_ans_list]
        
        # Get the student's answer list for this question (or empty list if not answered).
        student_ans_list = student_answers.get(question_num, [])
        
        # For a single-answer question: if more than one answer was marked, count as incorrect.
        if len(correct_ans_list) == 1:
            if len(student_ans_list) != 1:
                # Either no answer or more than one provided for a single-answer question.
                is_correct = False
            else:
                is_correct = (student_ans_list[0] == correct_ans_list[0])
        else:
            # For a multiple-answer question: the sets must match exactly.
            is_correct = (set(student_ans_list) == set(correct_ans_list))
        
        # If the answer is correct, add the corresponding point weight.
        if is_correct:
            total_score += float(points_mapping.get(question_num, 0.0))
    
    # Step 5: Convert the base64-encoded student_sheet into bytes.
    try:
        answer_sheet_bytes = base64.b64decode(student_sheet_b64)
    except Exception as e:
        return JsonResponse({'error': 'Invalid student_sheet encoding'}, status=400)
    
    # Step 6: Save the assessment result to the database.
    result = AssessmentResult.objects.create(
        assessment_id=assessment_id,
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        variant=variant,
        answers=student_answers,
        correct_answers=correct_answers,
        answer_sheet=answer_sheet_bytes,
        score=total_score
    )
    
    # Step 7: Return the assessment result.
    return JsonResponse({
        "result_id": result.id,
        "assessment_id": assessment_id,
        "score": total_score
    }, status=201)
