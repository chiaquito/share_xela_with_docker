from django import template

from items.models import Item


register = template.Library()

@register.simple_tag
def output_obj(content_object, object_id):
	"""
	申請者からアイテムオブジェクトを抽出する
	"""

	#obj = content_object.__model__.objects.get(id=object_id)
	#print(content_object.__model__)
	print(obj)
	return obj
    

"""
特定のobjectからmodelを抽出する方法を調べる

"""
