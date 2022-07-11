from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from article.models import (
    Article as ArticleModel,
    Comment as CommentModel,
    Board as BoardModel,
    Category as CategoryModel,
)

from rest_framework.permissions import IsAuthenticated
from article.serializers import (
    ArticleSerializer,
    CommentSerializer,
)

from rest_framework import permissions

class ArticleView(APIView):
    # permission_classes = [permissions.AllowAny]

    # 모든 게시글 리스팅
    def get(self, request):
        articles = list(ArticleModel.objects.all().order_by("-id"))
        result = ArticleSerializer(articles, many=True).data
        return Response(result) 

    # 게시글 작성
    def post(self, request):
        print(request.data)
        # article = ArticleModel(**request.data)
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
        return Response({'message': f'{user}님의 {title}게시글이 삭제되었습니다.'})

# url = 'article/<obj_id>/ article detail 페이지
class ArticleDetailView(APIView):
    permisiion_classes = [IsAuthenticated]

    def get(self, request, obj_id):
        article_detail = ArticleModel.objects.get(id=obj_id)
        article_detail_username = article_detail.author.username
        
        return Response(ArticleSerializer(article_detail).data)

class CommentView(APIView):
    # permission_classes = [IsAdminOrIsAuthenticatedReadOnly]
    permission_classes = [permissions.AllowAny]

    def get(self, request, article_id):
        return Response(CommentSerializer(article_id).data)

    # 댓글 작성
    def post(self, request, article_id):
        
        
        user = request.user
        print(user)
        request.data['article'] = ArticleModel.objects.get(id=article_id)
        contents = request.data.get('contents','')

        comment = CommentModel(
            article = request.data['article'],
            user = user,
            contents = contents,
        )

        comment.save()
        return Response({"message":"댓글 작성 완료!"})

    # 댓글 업데이트
    def put(self, request, comment_id):
        data = request.data
        comment = CommentModel.objects.get(id=comment_id)
        comment_serializer = CommentSerializer(comment, data, partial=True, context={"request": request})

        
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)

        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 삭제
    def delete(self, request, comment_id):
        
        obj = CommentModel.objects.get(id=comment_id)
        user = obj.user
        author = obj.article.author
        CommentModel.objects.get(id=comment_id).delete()

        if request.user == user:
            return Response({'message': f'{user}님의 댓글이 삭제되었습니다.'})
        
        elif request.user == author:
            return Response({'message': f'{user}님의 댓글이 삭제되었습니다.'})
        
        else:
            return Response({'error': '댓글 삭제 권한이 없습니다'})
    