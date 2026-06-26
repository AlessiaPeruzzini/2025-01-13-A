from dataclasses import dataclass

from model.gene import Gene


@dataclass
class Arco:
    gen1:Gene
    gen2: Gene
    peso: int