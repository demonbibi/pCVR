import xgboost as xgb
import pickle

# 加载数据
print("开始反序列化加载数据...")
with open('get_data_v4.3.data', 'rb') as train_data_file:
    data = pickle.loads(train_data_file.read())
print("加载结束...")

(x, y, test_id, test) = data
# print(test_id[2])
# 前90%是训练数据，后10%是测试数据,通过反向传播来进行预测！
split_at = len(x) - len(x) // 10
(x_train, x_val) = x[:split_at], x[split_at:]
(y_train, y_val) = y[:split_at], y[split_at:]

print(x_train)
print(y_train)

dtrain = xgb.DMatrix(x_train, label=y_train)
dval = xgb.DMatrix(x_val, label=y_val)
dtest = xgb.DMatrix(test, label=y_val)
evallist = [(dval, 'val')]

# specify parameters via map
param = {'booster': 'gbtree',
         'max_depth': 8,
         'max_delta_step': 8,
         'learning_rate': 0.1,
         'min_child_weight': 5,
         'objective': 'binary:logistic',
         'eval_metric': 'logloss',
         'subsample': 0.8,
         'colsample_bytree': 0.7,
         'n_estimators': 3000,
         'silent': True,
         'nthread ': 8
         }
num_round = 1000
bst = xgb.train(param, dtrain, num_round, evallist, verbose_eval=1, early_stopping_rounds=50)

bst.save_model('0002.model')
bst.dump_model('dump.raw.txt')  # dump model
score = bst.get_fscore()
print(score)
print("开始预测模型...")
predict = bst.predict(dtest)

print("开始将预测结果写入csv...")
with open('xgb_v1_submission.csv', 'w') as file:
    file.write('instanceID,prob\n')
    index = 0
    for one in predict[:]:
        file.write(str(test_id[index]) + ',' + str(one) + '\n')
        index += 1

print("结束...")
