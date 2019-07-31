# A module for RL trading #

## Example Training JSON

```json
{ 
    "_id" : ObjectId("5d3ed4ad1c793d1ddd9cb0e4"), 
    "training" : {
        "ent_coef" : 0.01, 
        "alpha" : 0.99, 
        "verbose" : NumberInt(1), 
        "n_steps" : NumberInt(5), 
        "full_tensorboard_log" : false, 
        "learning_rate" : 0.0007, 
        "_init_setup_model" : true, 
        "gamma" : 0.99, 
        "vf_coef" : 0.25, 
        "env" : {
            "name" : "di.factory.VecEnvFactory", 
            "target" : "stable_baselines.common.vec_env.DummyVecEnv", 
            "args" : [
                {
                    "context" : {
                        "trading_loss_pct" : 0.005, 
                        "initial_fundings" : 100000.0, 
                        "name" : "rltrader.context.TradingContext", 
                        "price_col_index" : NumberInt(3)
                    }, 
                    "space" : {
                        "max_steps" : NumberInt(10000), 
                        "random_start" : true, 
                        "history_lookback" : NumberInt(100), 
                        "data" : {
                            "name" : "rltrader.data.CsvFileDataFrameData", 
                            "path" : "/rldata/preprocessed/train_ZL000013_reduced.csv"
                        }, 
                        "action_space" : {
                            "name" : "gym.spaces.Discrete", 
                            "n" : NumberInt(3)
                        }, 
                        "name" : "rltrader.spaces.LookbackWindowDataSpace", 
                        "date_col" : "date"
                    }, 
                    "reward" : {
                        "name" : "rltrader.rewards.net_value_reward"
                    }, 
                    "name" : "rltrader.env.Env", 
                    "context_reset" : true
                }
            ]
        }, 
        "tensorboard_log" : null, 
        "policy" : {
            "target" : "stable_baselines.common.policies.MlpPolicy", 
            "name" : "di.factory.ModuleFactory", 
            "args" : [
                {

                }
            ]
        }, 
        "max_grad_norm" : 0.5, 
        "epsilon" : 0.00001, 
        "name" : "stable_baselines.A2C", 
        "lr_schedule" : "constant"
    }, 
    "total_timesteps" : NumberInt(201600), 
    "test_env" : {
        "context" : {
            "trading_loss_pct" : 0.005, 
            "initial_fundings" : 100000.0, 
            "name" : "rltrader.context.TradingContext", 
            "price_col_index" : NumberInt(3)
        }, 
        "space" : {
            "max_steps" : NumberInt(201600), 
            "random_start" : false, 
            "history_lookback" : NumberInt(100), 
            "data" : {
                "name" : "rltrader.data.CsvFileDataFrameData", 
                "path" : "/rldata/preprocessed/test_ZL000013_reduced.csv"
            }, 
            "action_space" : {
                "name" : "gym.spaces.Discrete", 
                "n" : NumberInt(3)
            }, 
            "name" : "rltrader.spaces.LookbackWindowDataSpace", 
            "date_col" : "date"
        }, 
        "reward" : {
            "name" : "rltrader.rewards.net_value_reward"
        }, 
        "name" : "rltrader.env.Env", 
        "context_reset" : false
    }
}
```

## Steps to  training

__1. Create a .env file__

   ```code
   DATA_DIR=<location of data on machine>
   ```
   
__2. Start training container to initialize containers and start database__

```shell
docker-compose -f "docker-compose-cpu.yml" up -d --build
```

__3. Login into Mongo DB__

```shell
docker exec -it rltrainingdb bash 
```

__4. Add traing session to mongodb__

Within the mongo shell execute the following commands:

```shell
root@ef48e9fb644f:/# mongo
MongoDB shell version v3.6.13
connecting to: mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("85d86369-7933-400a-8980-77d0bca05020") }
MongoDB server version: 3.6.13
Welcome to the MongoDB shell.
For interactive help, type "help".
> use training
switched to db training
> db.sessions.insertOne({ "training" : { "ent_coef" : 0.01, "alpha" : 0.99, "verbose" : 1, "n_steps" : 5, "full_tensorboard_log" : false, "learning_rate" : 0.0007, "_init_setup_model" : true, "gamma" :
0.99, "vf_coef" : 0.25, "env" : { "name" : "di.factory.VecEnvFactory", "target" : "stable_baselines.common.vec_env.DummyVecEnv", "args" : [ { "context" : { "trading_loss_pct" : 0.005, "initial_fundings" : 100000, "name" : "rltrader.context.TradingContext", "price_col_index" : 3 }, "space" : { "max_steps" : 10000, "random_start" : true, "history_lookback" : 100, "data" : { "name" : "rltrader.data.CsvFileDataFrameData", "path" : "/rldata/preprocessed/train_ZL000013_reduced.csv" }, "action_space" : { "name" : "gym.spaces.Discrete", "n" : 3 }, "name" : "rltrader.spaces.LookbackWindowDataSpace", "date_col" : "date" }, "reward" : { "name" : "rltrader.rewards.net_value_reward" }, "name" : "rltrader.env.Env", "context_reset" : true } ] }, "tensorboard_log" : null, "policy" : { "target" : "stable_baselines.common.policies.MlpPolicy", "name" : "di.factory.ModuleFactory", "args" : [ {  } ] }, "max_grad_norm" : 0.5, "epsilon" : 0.00001, "name" : "stable_baselines.A2C", "lr_schedule" : "constant" }, "total_timesteps" : 201600, "test_env" : { "context" : { "trading_loss_pct" : 0.005, "initial_fundings" : 100000, "name" : "rltrader.context.TradingContext", "price_col_index" : 3 }, "space" : { "max_steps" : 201600, "random_start" : false, "history_lookback" : 100, "data" : { "name" : "rltrader.data.CsvFileDataFrameData", "path" : "/rldata/preprocessed/test_ZL000013_reduced.csv" }, "action_space" : { "name"
: "gym.spaces.Discrete", "n" : 3 }, "name" : "rltrader.spaces.LookbackWindowDataSpace", "date_col" : "date" }, "reward" : { "name" : "rltrader.rewards.net_value_reward" }, "name" : "rltrader.env.Env", "context_reset" : false } })
```


__2. Restart training containers__

```shell
docker-compose -f "docker-compose-cpu.yml" up -d --build
```

___Training is then performed and the resulting model, training and history are persisted in Mongo GridFS___