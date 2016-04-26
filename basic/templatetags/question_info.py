from django import template
from qa.models import Question

register = template.Library()

@register.simple_tag
def get_question_qtext_from_qid(q_id):
    try:
        return Question.objects.get(id=q_id).q_text
    except Question.DoesNotExist:
        return 'Unknown'
