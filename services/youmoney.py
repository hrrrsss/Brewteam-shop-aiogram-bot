from yoomoney import Quickpay, Client

from config.config import settings

CLIENT_TOKEN = settings.TOKEN_YOO
client = Client(CLIENT_TOKEN)


def pay_yoomoney(tg_id: str, sum: int):
    label = f"order_{tg_id}"

    quickpay = Quickpay(
                receiver=settings.RECEIVER,
                quickpay_form="shop",
                targets=f"Оплата заказа {tg_id}",
                paymentType="AC",
                sum=sum,
                label=label
    )

    return quickpay.redirected_url, label


def check_yoomoney(label: str):
    history = client.operation_history(label=label)
    return bool(history.operations)

