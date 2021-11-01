from telegram import InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.utils.helpers import mention_markdown


def gen_message(
    text: str,
    in_list: list[tuple[int, str]],
    out_list: list[tuple[int, str]],
) -> dict[str, str | InlineKeyboardMarkup]:
    """
    Generates a message from the given text and the given lists of tuples.
    :param text: The text to be used.
    :param in_list: The list of tuples to be used as in.
    :param out_list: The list of tuples to be used as out.
    :return: The generated message.
    """
    in_text = "*In:*\n- " + "\n- ".join(
        mention_markdown(
            i[0],
            i[1],
        )
        for i in in_list
    )
    out_text = "*Out:*\n- " + "\n- ".join(
        mention_markdown(
            i[0],
            i[1],
        )
        for i in out_list
    )
    text = "\n\n".join((text, in_text, out_text))
    keyboard = [
        [
            InlineKeyboardButton(
                text="Add Me",
                callback_data={
                    "text": text,
                    "in": in_list,
                    "out": out_list,
                    "mode": "add",
                },
            ),
        ],
        [
            InlineKeyboardButton(
                text="Exclude Me",
                callback_data={
                    "text": text,
                    "in": in_list,
                    "out": out_list,
                    "mode": "exclude",
                },
            ),
        ],
    ]
    return {"text": text, "reply_markup": InlineKeyboardMarkup(keyboard)}


def in_or_out(
    mode: str,
    user: User,
    in_list: list[tuple[int, str]],
    out_list: list[tuple[int, str]],
) -> tuple[list[tuple[int, str]], list[tuple[int, str]], str]:
    """
    Modifies the lists as per requirement.
    :param mode: The mode to be used.
    :param in_list: The list of tuples to be used as in.
    """
    response = "No change in list!"
    usr = (int(user.id), user.full_name)
    if mode == "add":
        if usr not in in_list:
            in_list.append(usr)
        if usr in out_list:
            out_list.remove(usr)
        response = "Added you to the list!"
    elif mode == "exclude":
        if user.id not in out_list:
            out_list.append(usr)
        if user.id in in_list:
            in_list.remove(usr)
        response = "Excluded you from the list!"
    return in_list, out_list, response
