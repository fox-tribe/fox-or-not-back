from unicodedata import category
from django.core.paginator import Paginator
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from urllib import parse

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


from article.models import (
    Article as ArticleModel,
    Comment as CommentModel,
    Board as BoardModel,
    ArticleLike,
    CommentLike,
    CommentLikeBridge,
    ArticleLikeBridge,
    ArticleVoteBridge,
    Vote as VoteModel
)
from article.serializers import (
    ArticleSerializer,
    CommentSerializer,
)
# 게시판 별 게시글 페이지네이션
class ArticlePagination(APIView, LimitOffsetPagination):
    def get(self, request, format=None):
        board = request.query_params.getlist('board')[0]
        page = int(request.query_params.getlist('page')[0])
        # if board == 'HOT':
        #     articles = ArticleModel.objects.filter(board__name=board)
        #     print(articles)
        articles = ArticleModel.objects.filter(board__name=board).order_by("-id")[((page-1)*10):(page*10)]
        if board == 'HOT':
            all = list(ArticleModel.objects.all().values())
            articles_id = []
            for article in all:
                articles_id.append(article['id'])
            vote_counts = []
            for id in articles_id:
                vote_count = ArticleVoteBridge.objects.filter(article_id=id).count()
                if vote_count >= 1:
                    num = 0
                    num = num + 1
                vote_counts.append(vote_count)
            print(num)
            count_list = {name:value for name, value in zip(articles_id, vote_counts)}
            vote_rank = sorted(count_list.items(), key=lambda x: x[1], reverse=True)[:num]
            ranking = []
            for i in range(num):
                ranking.append(vote_rank[i][0])
            article_rank = ArticleModel.objects.filter(id__in = ranking)
            results = self.paginate_queryset(article_rank, request, view=self)
            serializer = ArticleSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            results = self.paginate_queryset(articles, request, view=self)
            serializer = ArticleSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)

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


# 댓글 페이지네이션 리스팅
class CommentPagination(APIView, LimitOffsetPagination):
    def get(self, request, format=None):
        comments = CommentModel.objects.all()
        results = self.paginate_queryset(comments, request, view=self)
        serializer = CommentSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

class ArticleView(APIView):
    permission_classes = [permissions.AllowAny]

    # 모든 게시글 리스팅
    def get(self, request):
        articles = list(ArticleModel.objects.all().order_by("-id"))
        result = ArticleSerializer(articles, many=True).data
        return Response(result) 

    # 게시글 작성
    def post(self, request):
        if request.user.is_anonymous:
            return Response({"error":"글 작성을 위해 로그인을 해주세요."})
        else:
            try:
                board = BoardModel.objects.get(name=request.data.get('board'))
                article = ArticleModel.objects.create(
                    article_author = request.user,
                    article_title = request.data.get('article_title',''),
                    article_contents = request.data.get('article_contents',''),
                    article_image = request.FILES['article_image'],
                    article_exposure_date = request.data.get('article_exposure_date',''),
                    board = board,
                )
            except:
                board = BoardModel.objects.get(name=request.data.get('board'))
                article = ArticleModel.objects.create(
                    article_author = request.user,
                    article_title = request.data.get('article_title',''),
                    article_contents = request.data.get('article_contents',''),
                    article_exposure_date = request.data.get('article_exposure_date',''),
                    board = board,
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

        if request.user == article.article_author or request.user.is_admin:
            article_serializer = ArticleSerializer(article, data=request.data, partial=True, context={"request": request})
            if article_serializer.is_valid():
                article_serializer.save()
                return Response(article_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"게시글 수정은 게시글 작성자만 할 수 있습니다."})

    # 게시물 삭제
    def delete(self, request, obj_id):
        article = ArticleModel.objects.get(id=obj_id)
        title = article.article_title 
        user = article.article_author
        if request.user == article.article_author or request.user.is_admin:
            ArticleModel.objects.get(id=obj_id).delete()
            return Response({'message': f'{user}님의 {title} 게시글이 삭제되었습니다.'})
        else:
            return Response({"message":"게시글 삭제는 게시글 작성자만 할 수 있습니다."})

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
        if request.user.is_anonymous:
            return Response({"error":"댓글 작성을 위해 로그인을 해주세요."})
        else:
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

        if request.user == comment.comment_author or request.user.is_admin:
            comment_serializer = CommentSerializer(comment, data, partial=True, context={"request": request})
            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(comment_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"댓글 수정은 댓글 작성자만 가능합니다."})

    # 댓글 삭제
    def delete(self, request, obj_id):
        comment = CommentModel.objects.get(id=obj_id)
        comment_author = comment.comment_author
        article_author = comment.article.article_author
        if request.user == comment.comment_author or request.user.is_admin or request.user == article_author:
            CommentModel.objects.get(id=obj_id).delete()
            return Response({'message': f'{comment_author}님의 댓글이 삭제되었습니다.'})
        else:
            return Response({'error': '댓글 삭제 권한이 없습니다'})

# 게시글 공감
class ArticleLikeView(APIView):
    authentication_classes = [JWTAuthentication]

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
    authentication_classes = [JWTAuthentication]

    # 게시글 투표 카운트
    def get(self, request, article_id):
        votes = ArticleVoteBridge.objects.filter(article_id=article_id)
        votes = list(votes.values())
        count = dict(fox=0, green=0, miss=0)
        for vote in votes:
            if vote['category'] == '폭스입니다':
                count['fox'] += 1
            elif vote['category'] == '그린라이트':
                count['green'] += 1
            else:
                count['miss'] += 1
        return Response(count)

    def post(self, request, article_id):
        vote = VoteModel.objects.create()
        article_title = ArticleModel.objects.get(id=article_id)
        all = list(ArticleVoteBridge.objects.all().values())
        article_vote = ArticleVoteBridge.objects.filter(user_id=request.user.id)
        vote_article = article_vote.filter(article_id=article_id)
        vote_article.delete()
        all_id = []
        for obj in all:
            all_id.append(obj['user_id'])
        try:
            article_vote = ArticleVoteBridge.objects.filter(user_id=request.user.id)
            if article_vote.category != request.data.get('category'):
                article_vote.delete()
                new_vote = ArticleVoteBridge(
                article_id = article_id,
                user_id = request.user.id,
                vote_id = vote.id,
                category = request.data.get('category',"")
            )
                new_vote.save()
                return Response({'message': f'{new_vote.category}로 재투표!'})
            elif article_vote.category == request.data.get('category'):
                return Response({'message': '이미 투표하셨습니다.'})
            else:
                article_vote = ArticleVoteBridge(
                    article_id = article_id,
                    user_id = request.user.id,
                    vote_id = vote.id,
                    category = request.data.get('category',"")
            )
                article_vote.save()
                return Response({'message': f'{article_vote.category}에 한표!'})
        except:
            article_vote = ArticleVoteBridge(
                article_id = article_id,
                user_id = request.user.id,
                vote_id = vote.id,
                category = request.data.get('category',"")
            )
            article_vote.save()
            return Response({'message': f'{article_vote.category}에 한표!'})
# 댓글 공감
class CommentLikeView(APIView):
    authentication_classes = [JWTAuthentication]

    # 댓글 공감 카운트
    def get(self, request, comment_id):
        like_count = CommentLikeBridge.objects.filter(comment_id=comment_id).count()
        return Response(like_count)

    def post(self, request, comment_id):
        like = CommentLike.objects.create()
        comment = CommentModel.objects.get(id=comment_id)
        contents = comment.comment_contents
        all = list(CommentLikeBridge.objects.all().values())
        all_id = []
        for obj in all:
            all_id.append(obj['user_id'])
        

        if request.user.id in all_id:
            # for i in all:
            #     id = i['comment_id']                
            try:
                CommentLikeBridge.objects.get(comment_id=comment_id)
                comment_like = CommentLikeBridge.objects.get(comment_id=comment_id)
                if comment_like.user_id == request.user.id:
                    comment_like.delete()
                    return Response({'message': f'{request.user}님께서 {contents[0:10]}...댓글에 공감을 취소하셨습니다.'})
            except:
                comment_like = CommentLikeBridge(
                    comment_id = comment_id,
                    user_id = request.user.id,
                    like_id = like.id,
                    category = request.data.get('category')
            )
                comment_like.save()
                return Response({'message': f'{request.user}님께서 {contents[0:10]}...댓글에 {comment_like.category}하셨습니다.'})
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
        like_rank = sorted(count_list.items(), key=lambda x: x[1], reverse=True)[:6]
        ranking = []
        for rank in range(len(like_rank)):
            if like_rank[rank][0] is not None: 
                ranking.append(like_rank[rank][0])
            else:
                pass
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
        like_rank = sorted(count_list.items(), key=lambda x: x[1], reverse=True)[:6]
        first = like_rank[0][0]
        second = like_rank[1][0]
        third = like_rank[2][0]
        forth = like_rank[3][0]
        fifth = like_rank[4][0]
        sixth = like_rank[5][0]
        ranking = [first, second, third, forth, fifth, sixth]
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
        vote_rank = sorted(count_list.items(), key=lambda x: x[1], reverse=True)[:6]
        rank_articles = []
        for rank in range(len(vote_rank)):
            ranker = vote_rank[rank][0]
            rank_articles.append(ranker)

        article_rank = ArticleModel.objects.filter(id__in = rank_articles)[::-1]
        return Response(ArticleSerializer(article_rank, many=True).data)

class SearchResult(APIView):
    permission_classes = [permissions.AllowAny]

    # 검색 결과 리스팅
    def post(self, request):
        keywords = request.data.get('search')
        type= request.data.get('type')
        # 내용 검색
        if type == '내용':
            searched_contents = ArticleModel.objects.filter(article_contents__contains=keywords)
            result = ArticleSerializer(searched_contents, many=True).data
            return Response(result) 
        # 작성자 검색
        elif type == '작성자':
            searched_authors = ArticleModel.objects.filter(article_author__username=keywords)
            result = ArticleSerializer(searched_authors, many=True).data
            return Response(result) 
        # 제목 + 내용 검색
        elif type == '제목+내용':
            searched_contents = ArticleModel.objects.filter(article_contents__contains=keywords)
            searched_titles = ArticleModel.objects.filter(article_title__contains=keywords)
            searched = searched_contents.union(searched_titles) 
            result = ArticleSerializer(searched, many=True).data
            return Response(result) 
        # 제목 검색
        else:
            searched_titles = ArticleModel.objects.filter(article_title__contains=keywords)
            result = ArticleSerializer(searched_titles, many=True).data
            return Response(result) 


# 메인페이지 게시판별 아티클 리스팅
class ArticleByBoard(APIView):

    def get(self, request):
        boards = request.query_params.getlist('boards', '')
        results = []
        for board in boards:
            articles = ArticleModel.objects.filter(board__name=board).order_by("-id")[:5]
            result = ArticleSerializer(articles, many=True).data
            results_data = {
                f"{board}" : result
            }
            results.append(results_data)
        return Response(results)

