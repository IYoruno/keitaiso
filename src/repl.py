import argparse
from pathlib import Path

import MeCab


def convert(text: str, tagger: MeCab.Tagger) -> str:
    result = []
    node = tagger.parseToNode(text)

    while node:
        if node.surface:
            features = node.feature.split(",")

            pos = features[0]
            conjugation = features[5] if len(features) > 5 else "*"

            if pos == "助詞" or pos == "補助記号":
                # 助詞・記号はそのまま
                result.append(node.surface)

            elif pos == "動詞":
                result.append("[動詞]")

            else:
                # 動詞・助詞・記号以外は品詞名
                result.append(f"[{pos}]")

        node = node.next

    return "".join(result)


def main():
    parser = argparse.ArgumentParser(
        description="MeCabの解析結果を品詞・活用形ラベルに変換します。"
    )
    parser.add_argument("input", help="入力するtxtファイル")
    parser.add_argument(
        "output",
        nargs="?",
        help="出力するtxtファイル（省略時: ./export/元のファイル名）",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = (
        Path(args.output)
        if args.output
        else Path("./export") / input_path.name
    )

    text = input_path.read_text(encoding="utf-8")
    tagger = MeCab.Tagger()

    # 改行を維持して各行を変換
    converted = "\n".join(
        convert(line, tagger) for line in text.splitlines()
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(converted, encoding="utf-8")

    print(f"変換完了: {input_path} -> {output_path}")


if __name__ == "__main__":
    main()