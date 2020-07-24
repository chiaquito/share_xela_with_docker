from django.shortcuts import render, redirect
from django.views.generic import View
# Create your views here.

from feedback.forms import FeedbackModelForm

from django.contrib.auth.models import User
from direct_messages.models     import DirectMessage
from items.models import Item

from config.constants import ViewName


"""
必要なビュー

ビューを作成するためのフォームを表示するビュー
フォームに入力されたデータに基づいてfeedbackを生成するビュー
"""



class ShowFeedbackFormView(View):

    def get(self, request, *args, **kwargs):
        """
        endpoint: 'feedback/create/'
        name: feedback:create

        機能:
        feedbackオブジェクト生成用のフォームを表示する


        他にもdirectmessageページにボタンを表示するかいなかの設定を追加したい。コレはDorectMessagelViewに加えるべきか？


        """

        """テスト項目
        未認証ユーザーによるアクセスはhomeにリダイレクトされる *1
        

        """
        if request.user.is_anonymous:
            return redirect(ViewName.HOME)

        context = {}
        #print(dir(self.request))
        dm_obj_pk   = self.kwargs["pk"]
        self.request.session["dm_obj_pk"] = dm_obj_pk

        evaluator = User.objects.get(username=request.user.username)
        form = FeedbackModelForm()
        context["form"] = form
        return render(request, 'feedback/show_feedback_form.html', context)




class FeedbackView(View):

    def post(self, request, *args, **kwargs):
        """機能
        Feedbackオブジェクトを生成する

        このpostメソッドで変更される内容は、
        DirectMessage.is_feedbacked_by_participantの変更
        DirectMessage.is_feedbacked_by_ownerの変更
        Feedbackオブジェクトの生成
        Profile.feedbackにFeedbackオブジェクトの追加
        
        endpoint: 'feedback/'
        name: 'feedback:feedback'
        """
        """テスト項目
        FeedbackModelFormのcontentが入力されていないときは?
        未認証ユーザーがpostアクセスした場合にはhomeにリダイレクトされる。(homeのテンプレート"config/home.html"が使われる) *1
        ユーザーがDirectMessageオブジェクトの主または参加者どちらでもない場合にはhomeにリダイレクトされる。*2
        入力されたフォームデータが不適切な場合には、feedback生成ページがリダイレクトされる。(テンプレートは'feedback/show_feedback_form.html') *3
        入力されたフォームデータが適切な場合には、アイテム詳細ページにリダイレクトされる。(テンプレートはTemplateKey.ITEM_DETAILが使われる)*4
        入力されたフォームデータが適切な場合にはFeedbackオブジェクトが生成される。*5
        アイテム記事の主がフィードバックを入力し、データが適切な場合には、dm_obj.is_feedbacked_by_ownerの値がTrueに変更される(前後チェック)*6
        アイテム記事の主がフィードバックを入力し、データが適切な場合には、アイテム記事参加者のProfile.feedbackにFeedbackオブジェクトが追加される。*7
        アイテム記事参加者がフィードバックを入力し、データが適切な場合には、dm_obj.is_feedbacked_by_participantの値がTrueに変更される(前後チェック)*8
        アイテム記事参加者がフィードバックを入力し、データが適切な場合には、アイテム記事主のProfile.feedbackにFeedbackオブジェクトが追加される。*9

        """
        try:
            dm_obj_pk = self.request.session["dm_obj_pk"]
            dm_obj = DirectMessage.objects.get(id=dm_obj_pk)
        except:
            return redirect(ViewName.HOME)



        
        if request.user.is_anonymous:
            return redirect(ViewName.HOME)

        # request.userがdm_objの取引相手でなければリダイレクトをかける
        if dm_obj.owner.user.username != request.user.username and dm_obj.participant.user.username != request.user.username:
            return redirect(ViewName.HOME)

        item_obj = Item.objects.get(direct_message=dm_obj)    

        form = FeedbackModelForm(request.POST)
        if form.is_valid():
            feedback_obj = form.save(commit=False)
            feedback_obj.evaluator = User.objects.get(username=request.user.username)
            feedback_obj.save()

            #取引相手のProfileオブジェクトのfeedbackに生成したfeedbackを追加する
            #取引相手を特定する
            if request.user.username == dm_obj.owner.user.username :
                dm_obj.participant.feedback.add(feedback_obj)
                dm_obj.is_feedbacked_by_owner = True
                dm_obj.save()

            elif request.user.username == dm_obj.participant.user.username :
                dm_obj.owner.feedback.add(feedback_obj)
                dm_obj.is_feedbacked_by_participant = True
                dm_obj.save()

            else:
                print("想定外のパターンを検出")
            return redirect("items:item_detail", item_obj.id)

        else:
            for ele in form:
                print(ele.error)
            return redirect("feedback:create", dm_obj_pk)



