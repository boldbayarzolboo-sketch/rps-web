from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Literal

from flask import Flask, render_template, request


Choice = Literal["rock", "paper", "scissors"]

app = Flask(__name__)

CHOICES: list[Choice] = ["rock", "paper", "scissors"]

BEATS: dict[Choice, Choice] = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}

@dataclass(frozen=True)
class RoundResult:
    player: Choice
    computer: Choice
    outcome: Literal["win", "lose", "draw"]
    message: str


def play_round(player_choice: Choice) -> RoundResult:
    computer_choice: Choice = random.choice(CHOICES)

    if player_choice == computer_choice:
        return RoundResult(
            player=player_choice,
            computer=computer_choice,
            outcome="draw",
            message="Тэнцлээ!",
        )

    if BEATS[player_choice] == computer_choice:
        return RoundResult(
            player=player_choice,
            computer=computer_choice,
            outcome="win",
            message="Та хожлоо!",
        )

    return RoundResult(
        player=player_choice,
        computer=computer_choice,
        outcome="lose",
        message="Та хожигдлоо!",
    )


@app.get("/")
def index():
    return render_template("index.html", result=None)


@app.post("/play")
def play():
    raw = (request.form.get("choice") or "").strip().lower()

    if raw not in CHOICES:
        # Хэрэглэгч хачин утга явуулбал хамгаалалт
        return render_template(
            "index.html",
            result={
                "error": "Сонголт буруу байна. Rock/Paper/Scissors-оос сонгоно уу."
            },
        ), 400

    result = play_round(raw)  # type: ignore[arg-type]
    return render_template("index.html", result=result)


if __name__ == "__main__":
    # debug=True хөгжүүлэлтийн үед
    app.run(host="127.0.0.1", port=5000, debug=True)
