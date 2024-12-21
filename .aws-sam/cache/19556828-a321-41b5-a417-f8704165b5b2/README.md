# iot-siginage-event-batch

## デプロイ手順
以下のセットアップが必要です。

* AWS SAM CLI - [Install the AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community).

セットアップが完了すると、以下のコマンドでデプロイが可能です。

```bash
sam build --use-container
sam deploy --guided
```

## ローカルでのテスト 
`PublishMessageFunction` では、AWSのSDKを使っているため事前に実行するために必要な認証情報を設定しておく必要があります。[Configuring settings for the AWS CLI](https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-configure.html) を参考に設定してください。

認証情報を設定したら、以下のコマンドでビルドを行います。コードの変更を反映するたびにビルドが必要です。

```bash
sam build --use-container
```

ローカルでLambda関数を実行するときには、`sam local invoke` コマンドを使って関数を呼び出します。

```bash
sam local invoke PublishMessageFunction --event events/event-cloudwatch-event.json
```

## リソースの削除

以下のコマンドでリソースを削除できます。

```bash
sam delete --stack-name iot-siginage-event-batch
```
