import base64
import typing

from pathlib import Path
from os import PathLike


ENCODING = "utf-8"


def save_participants_to(filename: PathLike, participants: typing.List[str]) -> None:
    """
    Save participants list to file in base64 encoding
    """
    with open(filename, "w+") as f:
        for message in participants:
            encoded_message = base64.b64encode(bytes(message, ENCODING))
            encoded_message = str(encoded_message, ENCODING)
            f.write(f"{encoded_message}\n")


def load_participants_from(filename: PathLike) -> typing.List[str]:
    """
    Loads participants list from file and decode they from base64
    """
    with open(filename, "r") as f:
        participants = f.readlines()
        
        for i in range(len(participants)):
            participant = participants[i].strip('\n')
            participant = base64.b64decode(participant).decode()
            participants[i] = participant

    return participants


if __name__ == "__main__":
    participants = ["Silvana", "DAnek", "Sofa", "Gleb", "Kok", "Off"]

    save_participants_to("PIZDA", participants)
    print(load_participants_from("PIZDA"))
