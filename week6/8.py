game_state = {
    "x": 100,
    "y": 200,
    "level": 3 
}
import json
f = open("game_state.txt", "w")
f.write(json.dumps(game_state))
f.close()