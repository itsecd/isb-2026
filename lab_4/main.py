import argparse
import json
import atak
import collision
import create
import packet


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "mode",
        choices=["create", "verify", "attack", "collision"],
        help="Режим работы программы",
    )

    parser.add_argument("-t", "--text", type=str, help="Текст сообщения")
    parser.add_argument("-k", "--key", type=str, help="Секретный ключ")
    parser.add_argument("-s", "--signature", type=str, help="HMAC подпись")
    parser.add_argument("-i", "--input", type=str, help="Путь к файлу для чтения данных")
    parser.add_argument("-o", "--output", type=str, help="Путь к файлу для сохранения JSON-пакета")

    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_arguments()

        if not args.key:
            raise ValueError("отсутствует секретный ключ.")

        match args.mode:

            case "create":
                text = ""
                if args.input:
                    with open(args.input, "r", encoding="utf-8") as f:
                        text = f.read().strip()
                elif args.text:
                    text = args.text
                else:
                    raise ValueError("не указан источник текста. Используйте флаг -t или -i.")

                print(f"Формирование подписи для сообщения: '{text}'")
                my_hmac = create.create(text, args.key)
                clean_packet = packet.transmit_packet(text, my_hmac)
                print(f"Сгенерированный HMAC-SHA256: {my_hmac}")

                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        json.dump(clean_packet, f, ensure_ascii=False, indent=4)
                    print(f"Сетевой пакет успешно сохранен в файл: {args.output}")

            case "verify":
                text, sig = "", ""
                if args.input:
                    with open(args.input, "r", encoding="utf-8") as f:
                        file_data = json.load(f)
                    text = file_data.get("data", "")
                    sig = file_data.get("hmac_hex", "")
                else:
                    text = args.text
                    sig = args.signature

                if not text or not sig:
                    raise ValueError(
                        "для верификации необходимы текст и подпись (или JSON-файл через флаг -i)."
                    )

                print("Запуск проверки целостности данных...")
                received_packet = {
                    "data": text,
                    "hmac_hex": sig,
                }
                is_valid = packet.verify_packet(received_packet, args.key)
                atak.detect(is_valid)

            case "attack":
                if not args.text:
                    raise ValueError("не указан новый текст для подмены.")

                print("Запуск симуляции компрометации пакета...")
                original_packet = atak.get_original_packet(args.key)

                spoiled_packet = atak.simulate_atak(
                    original_packet, args.text
                )
                is_spoiled_valid = packet.verify_packet(
                    spoiled_packet, args.key
                )
                atak.detect(is_spoiled_valid)

            case "collision":
                print(
                    "Запуск процесса подбора коллизии для усеченного HMAC..."
                )
                msg1, msg2, shared_hmac = collision.find_collision(args.key)
                print("\nКоллизия успешно обнаружена!")
                print(f"Первое сообщение:  {msg1}")
                print(f"Второе сообщение:  {msg2}")
                print(f"Общий усеченный HMAC: {shared_hmac}...")

            case _:
                print(f"Критическая ошибка: неизвестный режим {args.mode}")
                exit(1)

    except KeyboardInterrupt:
        print("\nПрограмма была принудительно остановлена пользователем.")
        exit(1)
    except ValueError as e:
        print(f"Ошибка: {e}")
        exit(1)
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        exit(1)