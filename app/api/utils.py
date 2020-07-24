from rest_framework.authtoken.models import Token




def getTokenFromHeader(self):
	"""
	機能:
	request Headerからtokenを取り出す関数


	args:
		-
	returns:
		str　トークンの文字列
	"""
	#token = self.request.META['HTTP_AUTHORIZATION'].split(" ")[1]
	headerInfo = self.request.META.get('HTTP_AUTHORIZATION', None)
	#print(headerInfo)
	if headerInfo == "Token":
		return None

	if headerInfo != None:
		token = headerInfo.split(" ")[1]
		return token

	elif headerInfo == None:
		return None



#tokenからUserオブジェクトを取得する
def getUserByToken(token):

	try:
		if token != None:
			user_obj = Token.objects.get(key=token).user
			return user_obj

		elif token == None:
			return None
	except:
		return None



#これはclassに格納したほうが良いかもしれない
def getItemDetailUrl(itemId):
	"""機能
	アイテム詳細ページのurlを作成する

	args:
		itemId:Intger ... 生成したまたは編集した記事のID
	returns:
		str: アイテム詳細ページのurl
	"""
	"""テスト項目(未検証)
	生成したオブジェクトに対するurlにアクセスすると詳細ページのテンプレートが使用されている
	生成したオブジェクトに対するurlにアクセスするとContextに生成したオブジェクトのidのオブジェクトが使われている
	"""


	urlTemplate = "https://sharexela.ga/items/item/{}/"
	url = urlTemplate.format(itemId)
	return url






