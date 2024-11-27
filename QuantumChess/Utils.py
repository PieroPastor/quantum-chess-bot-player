import math
import sys
import cirq
import copy
from copy import deepcopy
import random
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import os
bandera_de_comer_al_paso = False
bandera_de_enroque = False
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Desactiva optimizaciones oneDNN