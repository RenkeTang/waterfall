# -*- coding: utf-8 -*-
"""waterfall_chart"""


def waterfall(
    pth,
    index,
    data,
    total=None,
    base=0,
    title="waterfall chart",
    formatting="{:,.2f}",
    figsize=(12, 6),
    fontsize=14,
    x_lab="",
    y_lab="",
    rotation=0,
    positive_color=(255 / 255, 204 / 255, 153 / 255),
    minus_color=(191 / 255, 233 / 255, 217 / 255),
    total_color=(151 / 255, 115 / 255, 174 / 255),
):
    """
    waterfall_chart

    >> The following template is used for waterfall chart


    """
    import pandas as pd

    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    from textwrap import wrap

    pd.set_option("display.max_columns", None)

    # define format formatter
    def y_format(x, pos):
        "The two args are the value and tick position"
        return formatting.format(x)

    formatter = FuncFormatter(y_format)

    fig, ax = plt.subplots(figsize=figsize)
    ax.yaxis.set_major_formatter(formatter)

    if len(data) != len(index):
        print("error, the data and index are not with same length")

    if total is None:
        print("Please set which data is total.")
    # Store data and create a blank series to use for the waterfall
    trans = pd.DataFrame(data, index=index, columns=["amount"])

    def relative_total(x):
        return "total" if x in total else "relative"

    trans["cate"] = list(map(relative_total, list(trans.index)))

    trans["value"] = trans.apply(
        lambda x: 0 if x["cate"] == "total" else x["amount"], axis=1
    )

    trans["accum"] = trans["value"].cumsum().shift(1).fillna(0)

    def blank(x):
        return x["accum"] if x["cate"] == "relative" else 0

    trans["blank"] = trans.apply(blank, axis=1)

    def height(x):
        return x["value"] if x["cate"] == "relative" else x["accum"]

    trans["height"] = trans.apply(height, axis=1)

    def show_value(x):
        return x["value"] if x["cate"] == "relative" else x["height"]

    trans["show_value"] = trans.apply(show_value, axis=1)

    def color_set(x):
        if x["cate"] == "total":
            return total_color
        elif x["value"] > 0:
            return positive_color
        elif x["value"] < 0:
            return minus_color

    trans["color"] = trans.apply(color_set, axis=1)

    plt.bar(
        x=range(0, trans.shape[0]),
        height=trans["height"],
        width=0.6,
        bottom=trans["blank"],
        color=trans["color"],
    )

    yl = ax.get_ylim()[0]
    yh = ax.get_ylim()[1]

    y_rng = yh - yl

    def y_position(x):
        if x["cate"] == "total" or x["value"] < 0:
            return x["height"] + x["blank"] + y_rng / 40
        else:
            return x["height"] + x["blank"] - y_rng / 40

    trans["y_position"] = trans.apply(y_position, axis=1)

    if base == 0 and min(trans["y_position"]) < 0:
        ax.set_ylim([yl - y_rng / 10, yh + y_rng / 10])
    else:
        ax.set_ylim(base, yh + y_rng / 10)

    x_labels = ["\n".join(wrap(s, 7)) for s in list(trans.index)]

    plt.xticks(range(0, len(trans)), x_labels, rotation=rotation, fontsize=fontsize)

    # 对每个柱子标上具体值.
    for j, v in enumerate(trans["show_value"]):
        ax.text(
            x=j,
            y=trans["y_position"][j],
            s="{:.2f}".format(v),  # the text
            fontsize=fontsize,
            fontweight="normal",
            horizontalalignment="center",
            verticalalignment="center",
        )

    # axis labels
    plt.xlabel("\n" + x_lab, fontsize=fontsize)
    plt.ylabel(y_lab + "\n", fontsize=fontsize)

    # add base line and title
    plt.axhline(base, color="black", linewidth=0.6, linestyle="-")
    plt.title(title, fontsize=fontsize + 4)

    # hide spine on right and top
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    # ax.spines['bottom'].set_visible(False)

    plt.tight_layout()
    plt.savefig(pth + title + ".png")

    return plt

if __name__ =='__main__':
    import os
    pth = os.path.split(os.path.realpath(__file__))[0] + "/"

    index = ['Jan','Feb','Mar','Q1','Apr','May','Jun','H1']
    data = [100,-30,-7.5,-25,95,-7, 20, -30]
    total=['H1']

    waterfall(pth, index, data, total, title="waterfall_chart",)
