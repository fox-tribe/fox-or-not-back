from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from article.models import (
    Article as ArticleModel,
    Comment as CommentModel,
    Board as BoardModel,
    Category as CategoryModel,
    ArticleLike,
    CommentLike,
    CommentLikeBridge,
    ArticleLikeBridge,
    ArticleVoteBridge,
    Vote as VoteModel,
)
from article.serializers import (
    ArticleSerializer,
    CommentSerializer,
)



class ArticleView(APIView):
    # permission_classes = [permissions.AllowAny]

    # 모든 게시글 리스팅
    def get(self, request):
        articles = list(ArticleModel.objects.all().order_by("-id"))
        result = ArticleSerializer(articles, many=True).data
        return Response(result) 

    # 게시글 작성
    def post(self, request):
        board = BoardModel.objects.get(name=request.data.get('board'))
        category = CategoryModel.objects.get(name=request.data.get('article_category'))
        article = ArticleModel.objects.create(
            article_author = request.user,
            article_title = request.data.get('article_title',''),
            article_contents = request.data.get('article_contents',''),
            article_image = request.FILES,
            article_exposure_date = request.data.get('article_exposure_date',''),
            board = board,
            article_category = category,
        )
        if len(request.data.get('article_title','')) <= 1 :
            return Response({"error":"title이 1자 이하라면 게시글을 작성할 수 없습니다."})
        elif len(request.data.get('article_contents','')) <= 10 :
            return Response({"error":"contents가 10자 이하라면 게시글을 작성할 수 없습니다."}) 
        else:
            article.save()
            return Response({"message":"게시물 작성 완료!!"})

    # 게시물 업데이트
    def put(self, request, obj_id):
        article = ArticleModel.objects.get(id=obj_id)
        article_serializer = ArticleSerializer(article, data=request.data, partial=True, context={"request": request})
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시물 삭제
    def delete(self, request, obj_id):
        obj = ArticleModel.objects.get(id=obj_id)
        title = obj.article_title 
        user = obj.article_author
        ArticleModel.objects.get(id=obj_id).delete()
        return Response({'message': f'{user}님의 {title} 게시글이 삭제되었습니다.'})

# article detail 페이지 article/<obj_id>/detail/
class ArticleDetailView(APIView):

    def get(self, request, obj_id):        
        article = ArticleModel.objects.get(id=obj_id)
        return Response(ArticleSerializer(article).data)
class CommentView(APIView):

    def get(self, request, obj_id):
        return Response(CommentSerializer(obj_id).data)

    # 댓글 작성
    def post(self, request, obj_id):
        user = request.user
        request.data['article'] = ArticleModel.objects.get(id=obj_id)
        contents = request.data.get('comment_contents','')

        comment = CommentModel(
            article = request.data['article'],
            comment_author = user,
            comment_contents = contents,
        )
        comment.save()
        return Response({"message":"댓글 작성 완료!"})

    # 댓글 업데이트
    def put(self, request, obj_id):
        data = request.data
        comment = CommentModel.objects.get(id=obj_id)
        comment_serializer = CommentSerializer(comment, data, partial=True, context={"request": request})
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)

        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 삭제
    def delete(self, request, obj_id):
        obj = CommentModel.objects.get(id=obj_id)
        comment_author = obj.comment_author
        article_author = obj.article.article_author
        CommentModel.objects.get(id=obj_id).delete()

        if request.user == comment_author:
            return Response({'message': f'{comment_author}님의 댓글이 삭제되었습니다.'})
        
        elif request.user == article_author:
            return Response({'message': f'{comment_author}님의 댓글이 삭제되었습니다.'})
        
        else:
            return Response({'error': '댓글 삭제 권한이 없습니다'})
    

class CommentUserView(APIView):
    def get(self, request, comment_id):
        comment_detail = CommentModel.objects.get(id=comment_id)
        comment_detail_user = comment_detail.user.username
        return Response(comment_detail_user)

# 게시글 공감
class ArticleLikeView(APIView):

    def post(self, request, article_id):
        like = ArticleLike.objects.create()
        article_title = ArticleModel.objects.get(id=article_id)
        all = list(ArticleLikeBridge.objects.all().values())
        print(all)
        all_id = []
        for obj in all:
            all_id.append(obj['user_id'])
        

        if request.user.id in all_id:
            article_like = ArticleLikeBridge.objects.get(user_id=request.user.id)
            article_like.delete()
            return Response({'message': f'{request.user}님께서 {article_title.article_title}에 공감을 취소하셨습니다.'})
        else:
            article_like = ArticleLikeBridge(
                article_id = article_id,
                user_id = request.user.id,
                like_id = like.id,
                category = request.data.get('category')
        )
            article_like.save()
            return Response({'message': f'{request.user}님께서 {article_title.article_title}에 {article_like.category}하셨습니다.'})



# 게시글 투표
class ArticleVoteBridgeView(APIView):

    def post(self, request, article_id):
        vote = VoteModel.objects.create()
        article_title = ArticleModel.objects.get(id=article_id)
        all = list(ArticleVoteBridge.objects.all().values())
        
        all_id = []
        for obj in all:
            all_id.append(obj['user_id'])
        if request.user.id in all_id:
            article_vote = ArticleVoteBridge.objects.get(user_id=request.user.id)
            article_vote.delete()
            return Response({'message': f'{request.user}님께서 {article_title.article_title}에 투표를 취소하셨습니다.'})
        else:
            article_vote = ArticleVoteBridge(
                article_id = article_id,
                user_id = request.user.id,
                vote_id = vote.id,
                category = request.data.get('category',"")
        )
            article_vote.save()
            return Response({'message': f'{request.user}님께서 {article_title.article_title}에 {article_vote.category} 투표하셨습니다.'})


# 댓글 공감
class CommentLikeView(APIView):

    def post(self, request, comment_id):
        like = CommentLike.objects.create()
        comment = CommentModel.objects.get(id=comment_id)
        contents = comment.comment_contents
        all = list(CommentLikeBridge.objects.all().values())
        print(all)
        all_id = []
        for obj in all:
            all_id.append(obj['user_id'])
        

        if request.user.id in all_id:
            comment_like = CommentLikeBridge.objects.get(user_id=request.user.id)
            comment_like.delete()
            return Response({'message': f'{request.user}님께서 {contents[0:10]}...댓글에 공감을 취소하셨습니다.'})
        else:
            comment_like = CommentLikeBridge(
                comment_id = comment_id,
                user_id = request.user.id,
                like_id = like.id,
                category = request.data.get('category')
        )
            comment_like.save()
            return Response({'message': f'{request.user}님께서 {contents[0:10]}...댓글에 {comment_like.category}하셨습니다.'})


# 공감순 게시글 탑3 리스팅
class MostLikedArticleView(APIView):
    def get(self, request):
        articles = list(ArticleModel.objects.all().values())
        articles_id = []
        for article in articles:
            articles_id.append(article['id'])
        like_counts = []
        for id in articles_id:
            like_count = ArticleLikeBridge.objects.filter(article_id=id).count()
            like_counts.append(like_count)
        count_list = { name:value for name, value in zip(articles_id, like_counts)}
        like_rank = sorted(count_list.items(), key=lambda x: x[1], reverse=True)[:3]
        first = like_rank[0][0]
        second = like_rank[1][0]
        third = like_rank[2][0]
        ranking = [first, second, third]
        article_rank = ArticleModel.objects.filter(id__in = ranking)
        return Response(ArticleSerializer(article_rank, many=True).data)

       

# 공감순 댓글 탑3 리스팅
class MostLikedCommentView(APIView):
    def get(self, request):
        comments = list(CommentModel.objects.all().values())
        comments_id = []
        for comment in comments:
            comments_id.append(comment['id'])
        like_counts = []
        for id in comments_id:
            like_count = CommentLikeBridge.objects.filter(comment_id=id).count()
            like_counts.append(like_count)
        count_list = { name:value for name, value in zip(comments_id, like_counts)}
        like_rank = sorted(count_list.items(), key=lambda x: x[1], reverse=True)[:3]
        first = like_rank[0][0]
        second = like_rank[1][0]
        third = like_rank[2][0]
        ranking = [first, second, third]
        comment_rank = CommentModel.objects.filter(id__in = ranking)
        return Response(CommentSerializer(comment_rank, many=True).data)

# 투표순 탑3 리스팅
class MostVotedArticleView(APIView):
    def get(self, request):
        articles = list(ArticleModel.objects.all().values())
        articles_id = []
        for article in articles:
            articles_id.append(article['id'])
        vote_counts = []
        for id in articles_id:
            vote_count = ArticleVoteBridge.objects.filter(article_id=id).count()
            vote_counts.append(vote_count)
        count_list = { name:value for name, value in zip(articles_id, vote_counts)}
        vote_rank = sorted(count_list.items(), key=lambda x: x[1], reverse=True)[:3]
        first = vote_rank[0][0]
        second = vote_rank[1][0]
        third = vote_rank[2][0]
        ranking = [first, second, third]
        article_rank = ArticleModel.objects.filter(id__in = ranking)
        return Response(ArticleSerializer(article_rank, many=True).data)