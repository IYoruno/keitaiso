import MeCab

tagger = MeCab.Tagger()

def convert(text):
    result = []
    node = tagger.parseToNode(text)

    while node:
        if node.surface:
            features = node.feature.split(",")

            pos = features[0]  # 品詞
            conjugation = features[5] if len(features) > 5 else "*"

            if pos in ("助詞", "補助記号"):
                # 助詞・記号はそのまま
                result.append(node.surface)

            elif pos == "動詞":
                if conjugation.startswith("終止形"):
                    result.append("[動詞]")
                elif conjugation != "*":
                    # 「命令形」→「命令」
                    result.append(f"[{conjugation.removesuffix('形')}]")
                else:
                    result.append("[動詞]")

            else:
                result.append(f"[{pos}]")

        node = node.next

    return "".join(result)


text = "ぜったい いっぱい 輝け！未来を明るくしよう、するぞ！"
print(convert(text))