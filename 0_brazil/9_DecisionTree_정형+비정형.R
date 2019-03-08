############################## 의사결정나무
# 포인트 : data_anal.csv를 이용해서 의사결정나무 그려보기! 이것을 발판으로 추가 분석 실시!
# 입력 변수
# 배송변수 : del_period, del_period_psy, del_period_deadline_yn
# 정보변수 : product_description_length, product_photos_qty
# 가격변수 : payment_voucher_yn, order_freight_value, freight_value_proportion,
#            order_product_value
# 시간변수 : order_time_6, order_day, order_week_day_end,
#            review_ans_time_6, review_ans_day, review_ans_w_d_e, order_day_time_6
# 결제변수 : installments_yn, sim_installments_mean
# 기타변수 : review_ans_period, review_comment_yn
# 서비스변수 : seller_response_time
# 위치변수 : customer_state, customer_zip_code_prefix, seller_state, seller_zip_code_prefix

# 보류 변수 : del_period_rel, customer_city, city_type, order_product_range
# 결측치 문제로 분석에서 제외한 변수 : wgt_installments_mean
# 통제불가능하므로 분석에서 제외한 변수 : review_length


##### 목차
# 결측치 처리 방향 결정
#- del_period, del_period_psy, del_period_deadline_yn
#- 배송도착하지 않은 경우가 있어 결측치가 존재함함
#- 배송이 완료되지 않은 경우는 분석에서 제오
#- wgt_installments_mean
#- 1460개 존재
#- voucher로만 결제를 한 경우에는 NA가 나올 수 밖에 없도록 코딩함.....외
#- sim_installments_mean으로 어느정도 대체가능하므로 wgt_installments_mean은 일단 분석에서 제외함
#- seller_response_time
#- 17개 존재
#- order_arpoved_at 변수에 17개 NA가 존재해서 존재함
#- 17개 밖에 안되니까 row 제거함
#- seller_state, seller_zip_code_prefix
#- 17개 존재
#- NA를 하나의 레벨로 봐서 처리

# pn_review_score 팩터화

# 범주형 피처변수(15개)를 순서형 팩터화

# 분류 나무





# 2차 분류 나무
# 분석용 피처셋선택(5개 제외)
# 제외 : product_id, customer_unique_id, customer_zip_code_prefix, seller_zipcode_prefix, review_length

##### wd 설정
getwd()
setwd('C:\\Source\\Project_Brazil')

##### 라이브러리 준비
library("dplyr")
library("magrittr")

##### 데이터 로딩
raw <- read.csv("./data_merged/final_shit2.csv", header=T, sep=",",
                stringsAsFactors = F, # 팩터화 없이 일반적 로딩 
                strip.white = T, # 데이터 요소별 좌우 공백 제거 
                na.strings = "") # 데이터 중 ""표시부분 NA로 인식

##### 데이터 간단정보조회
str(raw)
summary(raw)
NROW(raw)

##### 결측치 처리 방향 결정
raw_delNA <- raw

is.na(raw_delNA)
colSums(is.na(raw_delNA))

# del_period(2295), de_period_psy(2295), del_period_deadline_yn(0)
# 일단 row 제거했으나, 이들이 결측되어있는 것이 무엇을 의미하는지 파악할 필요 있음
# 파생변수 생성할 때 del_period_psy가 0이상인 것은 True, 그외는 False로 하여서 del_period_psy가 NA인 경우도 del_period_deadline_yn이 False임
raw_delNA[is.na(raw_delNA$del_period), "del_period_deadline_yn"] %>% head()
raw_delNA <- raw_delNA[!is.na(raw_delNA$del_period),]
colSums(is.na(raw_delNA))

# wgt_installments_mean(1460)
#- 1460개 존재
#- voucher로만 결제를 한 경우에는 NA가 나올 수 밖에 없도록 코딩함.....
#- sim_installments_mean으로 어느정도 대체가능하므로 wgt_installments_mean은 일단 분석에서 제외함
raw_delNA[is.na(raw_delNA$wgt_installments_mean), "payment_voucher_yn"] %>% head()

# seller_response_time(17)
# 17개밖에 없으니까 row 제거
raw_delNA <- raw_delNA[!is.na(raw_delNA$seller_response_time),]
colSums(is.na(raw_delNA))

# seller_state, seller_zip_code_prefix
# NA가 17개 밖에 안되므로, 그냥 NA를 하나의 레벨로 보아서 팩터로 만들어 처리
colSums(is.na(raw_delNA))[colSums(is.na(raw_delNA))>0]


##### pn_review_score을 팩터로 변환
raw_factored <- raw_delNA
raw_factored$pn_review_score <- factor(raw_factored$pn_review_score, 
                                       levels=c("Positive", "Negative"), 
                                       labels=c("Positive", "Negative")) 

raw_factored %>% str



##### 범주형 피처변수를 순서형 팩터화
# 범주형 변수를 모두 (순서형)팩터로 변환

# 배송변수 : del_period, del_period_psy, del_period_deadline_yn
# 정보변수 : product_description_length, product_photos_qty
# 가격변수 : payment_voucher_yn, order_freight_value, freight_value_proportion,
#            order_product_value
# 시간변수 : order_time_6, order_day, order_week_day_end,
#            review_ans_time_6, review_ans_day, review_ans_w_d_e, order_day_time_6
# 결제변수 : installments_yn, sim_installments_mean
# 기타변수 : review_ans_period, review_comment_yn
# 서비스변수 : seller_response_time
# 위치변수 : customer_state, customer_zip_code_prefix, seller_state, seller_zip_code_prefix

raw_factored %>% group_by(votes_sat) %>% summarize(count = n(), countNegative = sum(pn_review_score == 'Negative'))
raw_factored %>% group_by(votes_before) %>% summarize(count = n(), countNegative = sum(pn_review_score == 'Negative'))
raw_factored %>% group_by(del_period_deadline_yn) %>% summarize(count = n(), countNegative = sum(pn_review_score == 'Negative'))
16000/76083
3319/14605

raw_factored[raw_factored$votes_before == 'True',]%>% select(pn_review_score,review_comment_message_english)

names <- c('del_period_deadline_yn', # 배송변수 중
           'payment_voucher_yn', # 가격변수 중
           'order_time_6', 'order_day', 'order_week_day_end', # 시간변수 중
           'review_ans_time_6', 'review_ans_day', 'review_ans_w_d_e', 'order_day_time_6',
           'installments_yn', # 결제변수 중
           'review_comment_yn', # 기타변수 중
           'customer_state', 'customer_zip_code_prefix','seller_state','seller_zip_code_prefix',
           'order_product_value_range',
           "votes_sat","votes_qual","votes_bro","votes_pack","votes_before","votes_delay",
           "votes_part","votes_wrong","votes_ret","votes_naa","votes_ss","votes_od","votes_etc") # 위치변수 중
#?factor


for (i in names) {
  subset <- raw_factored %>% group_by_at(i) %>% summarize(count = n(), countNegative = sum(pn_review_score == 'Negative'))
  subset$NegativeProb <- subset$countNegative / subset$count
  orderedLevels <- subset %>% arrange(desc(NegativeProb)) %>% select(i) %>% unlist(use.names = FALSE)
  #print(subset)
  
  raw_factored[,i] <- factor(raw_factored[,i],
                             levels = orderedLevels,
                             labels = orderedLevels,
                             exclude = NULL,
                             ordered = TRUE)
}


str(raw_factored)



############################################## final_shit 2###########################################

#########################1. 테스트

##### 데이터 분할
library(caret)

set.seed(1000)
intrain <- createDataPartition(y=raw_factored$pn_review_score, p = 0.7, list = FALSE)
intrain

train <- raw_factored[intrain, ]
test <- raw_factored[-intrain, ]
str(train)
str(test)

sum(test$pn_review_score == 'Positive')/NROW(test)
sum(train$pn_review_score == 'Positive')/NROW(train)

##### 의사결정나무

f1 <- pn_review_score ~ del_period + del_period_psy + del_period_deadline_yn +
  distance +
  order_product_value_range + freight_value_proportion + installments_yn +
  order_day+
  votes_sat+votes_qual+votes_bro+votes_pack+votes_before+votes_delay+
  votes_part+votes_wrong+votes_ret+votes_naa+votes_ss+votes_od+votes_etc

train %>% str
set.seed(100)
fit1 <- ctree(f1, data = train, controls = ctree_control(maxdepth = 4))
pdf('./images_tree/final2/1_tree.pdf', width = 30, height = 8)
plot(fit1, gp = gpar(fontsize=1))
dev.off()


pred <- predict(fit1, test)
pred
confusionMatrix(pred, test$pn_review_score)


###########################################2. 테스트 - votes_sat
##### 의사결정나무

f1 <- pn_review_score ~ del_period + del_period_psy + del_period_deadline_yn +
  distance +
  order_product_value_range + freight_value_proportion + installments_yn +
  order_day+
  votes_qual+votes_bro+votes_pack+votes_before+votes_delay+
  votes_part+votes_wrong+votes_ret+votes_naa+votes_ss+votes_od+votes_etc

train %>% str
set.seed(100)
fit1 <- ctree(f1, data = train, controls = ctree_control(maxdepth = 4))
pdf('./images_tree/final2/2_tree-sat.pdf', width = 30, height = 8)
plot(fit1, gp = gpar(fontsize=1))
dev.off()


pred <- predict(fit1, test)
pred
confusionMatrix(pred, test$pn_review_score)

###########################################3. 불만 투표만
##### 의사결정나무

f1 <- pn_review_score ~ votes_qual+votes_bro+votes_pack+votes_delay+
  votes_part+votes_wrong+votes_ret+votes_naa+votes_ss+votes_od+votes_etc

train %>% str
set.seed(100)
fit1 <- ctree(f1, data = train, controls = ctree_control(maxdepth = 4))
pdf('./images_tree/final2/3_tree_onlycomplainvotes.pdf', width = 30, height = 8)
plot(fit1, gp = gpar(fontsize=1))
dev.off()


pred <- predict(fit1, test)
pred
confusionMatrix(pred, test$pn_review_score)

###########################################4. 불만 투표만 - return
##### 의사결정나무

f1 <- pn_review_score ~ votes_qual+votes_bro+votes_pack+votes_delay+
  votes_part+votes_wrong+votes_naa+votes_ss+votes_od+votes_etc

train %>% str
set.seed(100)
fit1 <- ctree(f1, data = train, controls = ctree_control(maxdepth = 4))
pdf('./images_tree/final2/4_tree_onlycomplainvotes-ret.pdf', width = 30, height = 8)
plot(fit1, gp = gpar(fontsize=1))
dev.off()


pred <- predict(fit1, test)
pred
confusionMatrix(pred, test$pn_review_score)

