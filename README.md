# Proyecto-finalIA
# Guía de uso del proyecto

Este proyecto contiene la implementación del agente GAMPolicy para el juego Connect-4 como parte del Proyecto Final de Inteligencia Artificial. Para utilizarlo, primero debes clonar el repositorio con el comando `git clone https://github.com/Anacha1304/Proyecto-finalIA`, luego entrar a la carpeta con `cd Proyecto-finalIA`, y si deseas editar o visualizar el código desde Visual Studio Code puedes abrirlo usando `code .`. Antes de ejecutarlo, instala las dependencias requeridas utilizando `pip install -r requirements.txt`. El repositorio contiene los archivos principales del agente, el entorno del juego y un notebook con experimentos y gráficas.

Para ejecutar el agente solo necesitas importar la clase y montarla. Un ejemplo básico es:

```python
from policy import GAMPolicy
from connect4.game import Connect4

policy = GAMPolicy()
policy.mount(time_out=1)
game = Connect4(policy)
winner = game.play()
print("Ganador:", winner)
```


El notebook entrega.ipynb permite reproducir las pruebas, visualizaciones y análisis. Solo debes abrirlo y ejecutar las celdas en orden. Allí encontrarás experimentos como el desempeño contra un jugador aleatorio, la curva de aprendizaje, pruebas de eficiencia y la comparación entre diferentes profundidades de simulación. Puedes ajustar parámetros como num_partidas o rollout_depth para modificar los experimentos.

Las funciones principales disponibles en el notebook incluyen test_vs_random() para evaluar el agente contra un jugador aleatorio, test_learning_curve() para generar curvas de aprendizaje, optimize_rollout_depth() para comparar profundidades de simulación, y plot_results() para visualizar las gráficas generadas. Todas estas funciones ya están configuradas para usarse directamente.

Si deseas modificar el comportamiento del agente, puedes editar los parámetros dentro del archivo policy.py. Algunas configuraciones importantes son self.c_ucb para ajustar la exploración, self.rollout_depth para controlar cuántos pasos simula el agente en cada iteración, y valores como alpha o gamma que controlan la dinámica del aprendizaje.

Finalmente, se recomienda usar profundidades de simulación entre 10 y 18 para evitar timeouts, especialmente en evaluadores automáticos. Asegúrate siempre de ejecutar policy.mount() antes de iniciar un nuevo conjunto de partidas. Los resultados y gráficas se generan automáticamente cuando corres el notebook.
