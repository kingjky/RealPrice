## 개발노트



## Sub1



- 개발 환경 설정

~~~
python3 --version

## sub1으로 이동
python3 -m pip install -r requirements.txt
~~~

- 프로젝트 실행

~~~python
# 해당 프로젝트 폴더로 이동후 
# python 실행파일_이름
python parse.py
~~~

<hr>

### parse.py

>pandas 를 통한 데이터 전처리
>
>.json 데이터 파일을 읽어서 DataFrame 형태로 저장

- 필요한 스키마
  1. 음식점 (store)
  2. 리뷰(review)
  3. 유저(user)
  4. 메뉴(menu)
  5. 영업시간(bhour)

- data import

~~~python
# Step0 : DataFrame의 column 지정
store_columns = (
    "id",  # 음식점 고유번호
    "store_name",  # 음식점 이름
  	# ... (생략)
)

# Step1 : 파일 읽어오기
data = json.loads(f.read())

# Step2 : 테이블을 저장할 수 있는 list 생성
stores = []  # 음식점 테이블

# Step3 : data에서 필요한 요소 추출
# columns에 일치하는 데이터 요소를 추출하여 list에 append
for d in data:
   stores.append(
            [
                d["id"],
                d["name"],
                # ... (생략)
            ]
        )

# Step 4 : pandas의 DataFrame(2차원)형태로 저장
store_frame = pd.DataFrame(data=stores, columns=store_columns)
~~~



- 유저의 중복된 데이터 제거

> review -> user 데이터 추출
>
> 유저가 다양한 리뷰를 작성 ==> 중복 발생
>
> 중복 데이터를 제거하기 위해 Set 사용

~~~ python
# 중복된 유저 제거 (set)
# set -> list
users = list(set(map(tuple,users)))
~~~



### 결과화면

![1](img/sub1/1.png)  
![2](img/sub1/2.png)

<hr>

### analyze.py

> 저장한 DataFrame을 통해 필요한 데이터를 가공해서 사용

1. 최고 평점 음식점

~~~python
# review 와 store의 공통된 값(음식점 번호)를 통한 DataFrame 합치기
stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )

# 집계함수(평균)를 사용하기 위한 GroupBy
scores_group = stores_reviews.groupby(["store", "store_name"])

# 음식점의 평균 점수 + 높은 평균 점수별로 내림차순 정렬
scores = scores_group.mean() \
											.sort_values(by=["score"], ascending=False)
 
~~~

- 결과 화면

![3](/img/sub1/3.png)

> 최소 리뷰 개수 필터링을 못했음..

2. 리뷰 작성순 음식점

~~~python
# line 1. store, store_name으로 groupby
# line 2. store을 기준으로 count(), as cnt
# line 3. cnt기준으로 내림차순
scores_group = stores_reviews.groupby(["store", "store_name"]) \ 
                                				["store"].count().reset_index(name='cnt') \
  									.sort_values(by=["cnt"], ascending=False)
~~~

> 이때, 발생했던 에러 : count함수를 사용하고 결과 값을 'count'라고 별칭을 지어주고
>
> Main 에서 사용 ==> but 값을 불러오는데 제대로 된 결과값이 나오지 않음
>
> > count -> cnt로 바꿔서 출력하니 제대로 된 결과가 나왔음

- 결과화면

![4](/img/sub1/4.png)

3. 리뷰 작성순 유저

~~~python
users_group = users_reviews.groupby(["user"]) \
                            ["user"].count().reset_index(name='cnt')\
                            .sort_values(by=["cnt"], ascending=False)
~~~



- 결과화면

![5](/img/sub1/5.png)
