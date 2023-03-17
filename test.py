from mlops.logger import Lodge 

config = {"model": "pricing", "model_owner": "Juan Manoel", "squad": "mlops"}
console  = Lodge(config)

console.info({"test":"abobora"})

console.error({"test":"abobora2"})

