import random
import math

from django.shortcuts import render, get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import *
from posts.models import *
from comments.models import *
from mypage.models import *
from .serializers import *
from .pagination import PaginationHandlerMixin
from comments.serializers import CommentSerializer, RecommentSerializer
from django.db.models import Q, Count
from rest_framework.permissions import IsAuthenticated


# 댓글순(defalut) 홈화면 - 가장 좋아요 많이 받은 가사 5개, 댓글 Top10
class HomeCommentsView(views.APIView):
    def get(self, request):
        # 가장 좋아요 많이 받은 게시물 5개
        most_likes = Post.objects.order_by("-likes_count")[:5]
        most_likes_seri = LikesSerializer(most_likes, many=True)

        # 댓글순으로 Top10 게시물
        top_comments = Post.objects.annotate(
            comments_count=Count("comment") + Count("comments")
        ).order_by("-comments_count")[:10]
        top_comments_seri = TopSerializer(top_comments, many=True)

        data = {
            "Likes": most_likes_seri.data,
            "LankingList": top_comments_seri.data,
        }

        return Response(
            {"message": "홈 댓글순 조회 성공", "data": data}, status=status.HTTP_200_OK
        )


# 최신순 홈화면
class HomeLatestView(views.APIView):
    def get(self, request):
        # 가장 좋아요 많이 받은 게시물 5개
        most_likes = Post.objects.order_by("-likes_count")[:5]
        most_likes_seri = LikesSerializer(most_likes, many=True)

        # 최신순으로 Top 10 게시물
        top_latest = Post.objects.order_by("-created_at")[:10]
        top_latest_seri = TopSerializer(top_latest, many=True)

        data = {
            "Likes": most_likes_seri.data,
            "LankingList": top_latest_seri.data,
        }

        return Response(
            {"message": "홈 최신순 조회 성공", "data": data}, status=status.HTTP_200_OK
        )


# 좋아요순 홈화면
class HomeLikesView(views.APIView):
    def get(self, request):
        # 가장 좋아요 많이 받은 게시물 5개
        most_likes = Post.objects.order_by("-likes_count")[:5]
        most_likes_seri = LikesSerializer(most_likes, many=True)

        # 좋아요순으로 Top 10 게시물
        top_likes = Post.objects.order_by("-likes_count")[:10]
        top_likes_seri = TopSerializer(top_likes, many=True)

        data = {
            "Likes": most_likes_seri.data,
            "LankingList": top_likes_seri.data,
        }

        return Response(
            {"message": "홈 좋아요순 조회 성공", "data": data},
            status=status.HTTP_200_OK,
        )


"""
#추천페이지
class RecommendView(views.APIView):
    def get(self, request):
        all_posts = Post.objects.all()
        ran_size = min(60, len(all_posts))  # 리스트 크기보다 크지 않은 값을 선택
        random_posts = random.sample(list(all_posts), ran_size)
        random_posts_seri = RecommendSerializer(random_posts,many=True)

        return Response({'message': '추천게시물 조회 성공', 'data': random_posts_seri.data}, status=status.HTTP_200_OK)
"""


# 추천시스템 1안으로 수정
class RecommendView(views.APIView):
    def get(self, request):
        # 로그인 했을 때 -> 새로운 추천시스템(1안)
        if request.user.is_authenticated:  # Check if the user is authenticated
            page = int(request.GET.get('page'))
            user = request.user
            page_size =10
            if (page==1):
                emotion_counts = [0] * 12 
                # (1)내가 저장한 (북마크) 게시물의 감정 가져오기
                scraped_posts = user.scraped_posts.all()
                for post in scraped_posts:
                    emotion_index = post.sings_emotion
                    emotion_counts[emotion_index] += 1
                # (2)내가 감정을 남긴 게시물의 감정 가져오기
                emo_emotions = Emotion.objects.filter(emo_user=user).all()
                for emotion in emo_emotions:
                    emotion_index = emotion.emo_post.sings_emotion
                    emotion_counts[emotion_index] += 1
                # (3)내가 댓글을 남긴 게시물의 감정 가져오기
                user_comments = Comment.objects.filter(author=user).all()
                for comment in user_comments:
                    emotion_index = comment.post.sings_emotion
                    emotion_counts[emotion_index] += 1
                # (4)내가 남긴 가사의 감정 가져오기
                written_sings = Post.objects.filter(author=user).all()
                for sing in written_sings:
                    emotion_index = sing.sings_emotion
                    emotion_counts[emotion_index] += 1
                # 1~4위 감정 추출
                max_emotion_indices = sorted(
                    range(len(emotion_counts)),
                    key=lambda i: emotion_counts[i],
                    reverse=True
                )
                selected_indices = []
                for index in max_emotion_indices:
                    if emotion_counts[index] != 0:
                        selected_indices.append(index)
                selected_indices = sorted(selected_indices, reverse=True)[:4]

                # 집계된 감정이 없는 경우
                if not selected_indices: 
                    all_posts = Post.objects.all()
                    recommended_posts = list(all_posts.values_list('id', flat=True))[:100]
                    random.shuffle(recommended_posts)

                    user.recomlist =  ','.join(map(str, recommended_posts))
                    user.save()
                    
                    total_pages = math.ceil(len(recommended_posts) / page_size)
                    recommended_posts = recommended_posts[:10]
                    
                    recommended_posts_obj = []
                    for post_id in recommended_posts:
                        post = Post.objects.get(id=post_id)
                        recommended_posts_obj.append(post)

                    recommended_posts_seri = RecommendSerializer(recommended_posts_obj, many=True)

                    return Response(
                        {
                            "message": "감정 기록이 없는 로그인 유저 추천게시물 조회 성공",
                            "data": recommended_posts_seri.data,
                            "page": page,
                            "totalPage":total_pages,
                            "view": len(recommended_posts_obj)
                        },
                        status=status.HTTP_200_OK,
                    )
                
                # 나머지 감정 추출
                all_indices = list(range(12))
                remaining_indices = [i for i in all_indices if i not in selected_indices]
                
                # 추천시스템에 의한 추천 Post list
                max_size_1 = 70
                max_size_2 = 30

                recommended_posts_70_percent = Post.objects.filter(
                    sings_emotion__in=selected_indices
                )
                recommended_posts_30_percent = Post.objects.filter(
                    sings_emotion__in=remaining_indices
                )
                if(recommended_posts_70_percent.count()<max_size_1): 
                    max_size_1=recommended_posts_70_percent.count()
                    max_size_2=min((int)(max_size_1*3/7),recommended_posts_30_percent.count())

                shuffled_70_posts = list(recommended_posts_70_percent.values_list('id', flat=True))
                random.shuffle(shuffled_70_posts)
                posts_for_70 = shuffled_70_posts[:max_size_1]

                shuffled_30_posts = list(recommended_posts_30_percent.values_list('id', flat=True))
                random.shuffle(shuffled_30_posts)
                posts_for_30 = shuffled_30_posts[:max_size_2]

                recommended_posts = posts_for_70 + posts_for_30
                random.shuffle(recommended_posts)

                # 나머지는 랜덤으로 반환
                total_posts = min(100, Post.objects.count())
                remaining_size = total_posts - len(recommended_posts)
                remaining_posts = set()

                # 중복되지 않는 Post 추가
                all_post_ids = list(Post.objects.values_list('id', flat=True))
                while remaining_size > 0:
                    random_post_id = random.choice(all_post_ids)
                    if random_post_id not in recommended_posts:
                        remaining_posts.add(random_post_id)
                        remaining_size -= 1
                remaining_posts = list(remaining_posts)
                random.shuffle(remaining_posts)

                recommended_posts += remaining_posts

                user.recomlist =  ','.join(map(str, recommended_posts))
                user.save()
                
                total_pages = math.ceil(len(recommended_posts) / page_size)
                recommended_posts = recommended_posts[:10]
                
                recommended_posts_obj = []
                for post_id in recommended_posts:
                    post = Post.objects.get(id=post_id)
                    recommended_posts_obj.append(post)

                recommended_posts_seri = RecommendSerializer(recommended_posts_obj, many=True)

                return Response(
                    {
                        "message": "로그인 유저 추천게시물 조회 성공",
                        "data": recommended_posts_seri.data,
                        "page": page,
                        "totalPage":total_pages,
                        "view": len(recommended_posts_obj)
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                recomlist_text = user.recomlist
                recomlist = recomlist_text.split(',')
                total_pages = math.ceil(len(recomlist) / page_size)
                
                start_index = (page - 1) * page_size
                end_index = page * page_size
                recommended_posts = recomlist[start_index:end_index]
                recommended_posts_obj = []
                for post_id in recommended_posts:
                    post = Post.objects.get(id=post_id)
                    recommended_posts_obj.append(post)
                recommended_posts_seri = RecommendSerializer(recommended_posts_obj, many=True)
                return Response(
                    {
                        "message": "로그인 유저 추천게시물 조회 성공",
                        "data": recommended_posts_seri.data,
                        "page": page,
                        "totalPage":total_pages,
                        "view": len(recommended_posts_obj)
                    },
                    status=status.HTTP_200_OK,
                )

        # 로그인 안했을 때 -> 기존의 추천 시스템(랜덤 pk값으로 추천 게시물 선정)
        else:
            all_posts = Post.objects.all()
            ran_size = min(10, len(all_posts))  # 리스트 크기보다 크지 않은 값을 선택
            random_posts = random.sample(list(all_posts), ran_size)
            random_posts_seri = RecommendSerializer(random_posts, many=True)

            return Response(
                {
                    "message": "비로그인 유저 추천게시물 조회 성공",
                    "data": random_posts_seri.data,
                },
                status=status.HTTP_200_OK,
            )
        
# 카드 추천 시스템 TEST
class RecommendTestView(views.APIView):
    def get(self, request):
        # 로그인 했을 때 -> 새로운 추천시스템(1안)
        if request.user.is_authenticated:  # Check if the user is authenticated
            # page = int(request.GET.get('page'))
            user = request.user
            # page_size =10
            # if (page==1):

            emotion_counts = [0] * 12 
            # (1)내가 저장한 (북마크) 게시물의 감정 가져오기
            scraped_posts = user.scraped_posts.all()
            for post in scraped_posts:
                emotion_index = post.sings_emotion
                emotion_counts[emotion_index] += 1
            # (2)내가 감정을 남긴 게시물의 감정 가져오기
            emo_emotions = Emotion.objects.filter(emo_user=user).all()
            for emotion in emo_emotions:
                emotion_index = emotion.emo_post.sings_emotion
                emotion_counts[emotion_index] += 1
            # (3)내가 댓글을 남긴 게시물의 감정 가져오기
            user_comments = Comment.objects.filter(author=user).all()
            for comment in user_comments:
                emotion_index = comment.post.sings_emotion
                emotion_counts[emotion_index] += 1
            # (4)내가 남긴 가사의 감정 가져오기
            written_sings = Post.objects.filter(author=user).all()
            for sing in written_sings:
                emotion_index = sing.sings_emotion
                emotion_counts[emotion_index] += 1
            # 1~4위 감정 추출
            max_emotion_indices = sorted(
                range(len(emotion_counts)),
                key=lambda i: emotion_counts[i],
                reverse=True
            )
            selected_indices = []
            for index in max_emotion_indices:
                if emotion_counts[index] != 0:
                    selected_indices.append(index)
            selected_indices = sorted(selected_indices, reverse=True)[:4]

            # 집계된 감정이 없는 경우
            if not selected_indices: 
                all_posts = Post.objects.all()
                recommended_posts = list(all_posts.values_list('id', flat=True))[:100]
                random.shuffle(recommended_posts)

                # user.recomlist =  ','.join(map(str, recommended_posts))
                # user.save()
                
                # total_pages = math.ceil(len(recommended_posts) / page_size)
                # recommended_posts = recommended_posts[:10]
                
                # recommended_posts_obj = []
                # for post_id in recommended_posts:
                #     post = Post.objects.get(id=post_id)
                #     recommended_posts_obj.append(post)

                # recommended_posts_seri = RecommendSerializer(recommended_posts_obj, many=True)

                # return Response(
                #     {
                #         "message": "감정 기록이 없는 로그인 유저 추천게시물 조회 성공",
                #         "data": recommended_posts_seri.data,
                #         "page": page,
                #         "totalPage":total_pages,
                #         "view": len(recommended_posts_obj)
                #     },
                #     status=status.HTTP_200_OK,
                # )
                return Response(
                    {
                        "message": "감정 기록이 없는 로그인 유저 추천게시물 조회 성공",
                        "data": recommended_posts_seri.data,
                        "view": len(recommended_posts_obj)
                    },
                    status=status.HTTP_200_OK,
                )
                
            
            # 나머지 감정 추출
            all_indices = list(range(12))
            remaining_indices = [i for i in all_indices if i not in selected_indices]
            
            # 추천시스템에 의한 추천 Post list
            max_size_1 = 70
            max_size_2 = 30

            recommended_posts_70_percent = Post.objects.filter(
                sings_emotion__in=selected_indices
            )
            recommended_posts_30_percent = Post.objects.filter(
                sings_emotion__in=remaining_indices
            )
            if(recommended_posts_70_percent.count()<max_size_1): 
                max_size_1=recommended_posts_70_percent.count()
                max_size_2=min((int)(max_size_1*3/7),recommended_posts_30_percent.count())

            shuffled_70_posts = list(recommended_posts_70_percent.values_list('id', flat=True))
            random.shuffle(shuffled_70_posts)
            posts_for_70 = shuffled_70_posts[:max_size_1]

            shuffled_30_posts = list(recommended_posts_30_percent.values_list('id', flat=True))
            random.shuffle(shuffled_30_posts)
            posts_for_30 = shuffled_30_posts[:max_size_2]

            recommended_posts = posts_for_70 + posts_for_30
            random.shuffle(recommended_posts)

            # 나머지는 랜덤으로 반환
            total_posts = min(100, Post.objects.count())
            remaining_size = total_posts - len(recommended_posts)
            remaining_posts = set()

            # 중복되지 않는 Post 추가
            all_post_ids = list(Post.objects.values_list('id', flat=True))
            while remaining_size > 0:
                random_post_id = random.choice(all_post_ids)
                if random_post_id not in recommended_posts:
                    remaining_posts.add(random_post_id)
                    remaining_size -= 1
            remaining_posts = list(remaining_posts)
            random.shuffle(remaining_posts)

            recommended_posts += remaining_posts

            # user.recomlist =  ','.join(map(str, recommended_posts))
            # user.save()
            
            # total_pages = math.ceil(len(recommended_posts) / page_size)
            # recommended_posts = recommended_posts[:10]
            
            recommended_posts_obj = []
            for post_id in recommended_posts:
                post = Post.objects.get(id=post_id)
                recommended_posts_obj.append(post)

            recommended_posts_seri = RecommendSerializer(recommended_posts_obj, many=True)

            return Response(
                {
                    "message": "로그인 유저 추천게시물 조회 성공",
                    "data": recommended_posts_seri.data,
                    # "page": page,
                    # "totalPage":total_pages,
                    "view": len(recommended_posts_obj)
                },
                status=status.HTTP_200_OK,
            )
            # else:
            #     recomlist_text = user.recomlist
            #     recomlist = recomlist_text.split(',')
            #     total_pages = math.ceil(len(recomlist) / page_size)
                
            #     start_index = (page - 1) * page_size
            #     end_index = page * page_size
            #     recommended_posts = recomlist[start_index:end_index]
            #     recommended_posts_obj = []
            #     for post_id in recommended_posts:
            #         post = Post.objects.get(id=post_id)
            #         recommended_posts_obj.append(post)
            #     recommended_posts_seri = RecommendSerializer(recommended_posts_obj, many=True)
            #     return Response(
            #         {
            #             "message": "로그인 유저 추천게시물 조회 성공",
            #             "data": recommended_posts_seri.data,
            #             "page": page,
            #             "totalPage":total_pages,
            #             "view": len(recommended_posts_obj)
            #         },
            #         status=status.HTTP_200_OK,
            #     )

        # 로그인 안했을 때 -> 기존의 추천 시스템(랜덤 pk값으로 추천 게시물 선정)
        else:
            all_posts = Post.objects.all()
            # ran_size = min(10, len(all_posts))  # 리스트 크기보다 크지 않은 값을 선택
            ran_size = min(100, len(all_posts))
            random_posts = random.sample(list(all_posts), ran_size)
            random_posts_seri = RecommendSerializer(random_posts, many=True)

            return Response(
                {
                    "message": "비로그인 유저 추천게시물 조회 성공",
                    "data": random_posts_seri.data,
                },
                status=status.HTTP_200_OK,
            )



class BoothPagination(PageNumberPagination):
    page_size = 15


# 가사 검색 최신순 정렬
class SearchLatestView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination

    def get(self, request):
        keyword = request.GET.get("keyword")
        emo = request.GET.get("emo")

        posts = Post.objects.all()

        if keyword:
            posts = posts.filter(Q(lyrics__icontains=keyword))

        if emo:
            # posts = posts.filter(Q(sings_emotion__iexact=emo))
            posts = posts.filter(Q(sings_emotion__iexact=str(emo)))

        posts_latest = posts.order_by("-created_at")

        total = posts_latest.__len__()
        total_page = math.ceil(total / 15)
        posts_latest = self.paginate_queryset(posts_latest)

        posts_latest_seri = SearchSerializer(posts_latest, many=True)

        return Response(
            {
                "message": "최신순 가사 검색 성공",
                "total": total,
                "total_page": total_page,
                "current_page": self.current_page,
                "data": posts_latest_seri.data,
            },
            status=status.HTTP_200_OK,
        )


# 가사 검색 좋아요순 정렬
class SearchLikesView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination

    def get(self, request):
        keyword = request.GET.get("keyword")
        emo = request.GET.get("emo")

        posts = Post.objects.all()

        if keyword:
            posts = posts.filter(Q(lyrics__icontains=keyword))

        if emo:
            posts = posts.filter(Q(sings_emotion__iexact=str(emo)))

        posts_likes = posts.order_by("-likes_count")

        total = posts_likes.__len__()
        total_page = math.ceil(total / 15)
        posts_likes = self.paginate_queryset(posts_likes)

        posts_likes_seri = SearchSerializer(posts_likes, many=True)

        return Response(
            {
                "message": "좋아요순 가사 검색 성공",
                "total": total,
                "total_page": total_page,
                "current_page": self.current_page,
                "data": posts_likes_seri.data,
            },
            status=status.HTTP_200_OK,
        )


# 가사 검색 댓글순 정렬
class SearchCommentsView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination

    def get(self, request):
        keyword = request.GET.get("keyword")
        emo = request.GET.get("emo")

        posts = Post.objects.all()

        if keyword:
            posts = posts.filter(Q(lyrics__icontains=keyword))

        if emo:
            posts = posts.filter(Q(sings_emotion__iexact=str(emo)))

        posts_comments = posts.annotate(
            comments_count=Count("comment") + Count("comments")
        ).order_by("-comments_count")

        total = posts_comments.__len__()
        total_page = math.ceil(total / 15)
        posts_comments = self.paginate_queryset(posts_comments)

        posts_comments_seri = SearchSerializer(posts_comments, many=True)

        return Response(
            {
                "message": "댓글순 가사 검색 성공",
                "total": total,
                "total_page": total_page,
                "current_page": self.current_page,
                "data": posts_comments_seri.data,
            },
            status=status.HTTP_200_OK,
        )


"""
#감정태그 최신순 정렬
class SearchEmoLatestView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination
    
    def get(self, request):
        emo = request.GET.get('emo')

        posts = Post.objects.filter(Q(sings_emotion__iexact=str(emo)))
        
        posts_latest = posts.order_by('-created_at')

        total = posts_latest.__len__()
        total_page = math.ceil(total/15)
        posts_latest = self.paginate_queryset(posts_latest)
        posts_latest_seri = SearchSerializer(posts_latest, many=True)
        
        return Response({'message': '감정태그 최신순 검색 성공', 'total': total, 'total_page' : total_page, 'current_page': self.current_page, 'data': {"sings": posts_latest_seri.data}}, status=status.HTTP_200_OK)
        

#감정태그 좋아요순 정렬
class SearchEmoLikesView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination
    
    def get(self, request):
        emo = request.GET.get('emo')
        
        posts = Post.objects.filter(Q(sings_emotion__iexact=str(emo)))
        
        posts_likes = posts.order_by('-likes_count')

        total = posts_likes.__len__()
        total_page = math.ceil(total/15)
        posts_likes = self.paginate_queryset(posts_likes)
        posts_likes_seri = SearchSerializer(posts_likes, many=True)
        
        return Response({'message': '감정태그 좋아요순 검색 성공', 'total': total, 'total_page' : total_page, 'current_page': self.current_page, 'data': {"sings": posts_likes_seri.data}}, status=status.HTTP_200_OK)
        

#감정태그 댓글순 정렬
class SearchEmoCommentsView(views.APIView, PaginationHandlerMixin):
    pagination_class = BoothPagination
    
    def get(self, request):
        emo = request.GET.get('emo')
        
        posts = Post.objects.filter(Q(sings_emotion__iexact=str(emo)))
     
        posts_comments = posts.annotate(comments_count=Count('comment')+Count('comments')).order_by('-comments_count')
        
        total = posts_comments.__len__()
        total_page = math.ceil(total/15)
        posts_comments = self.paginate_queryset(posts_comments)
        posts_comments_seri = SearchSerializer(posts_comments, many=True)
        
        return Response({'message': '감정태그 댓글순 검색 성공', 'total': total, 'total_page' : total_page, 'current_page': self.current_page, 'data': {"sings": posts_comments_seri.data}}, status=status.HTTP_200_OK)
"""
