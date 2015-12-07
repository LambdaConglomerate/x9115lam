from os import *
from shutil import *
import Spread

def runner():
  frontier_path = './obtained/'
  runner_path = './Obtained_PF/'
  frontier_list = listdir(frontier_path)
  runner_list = listdir(runner_path)

  for deleted in runner_list:
    remove(runner_path + deleted)

  for f in frontier_list:
    # print frontier_path + f
    copy(frontier_path + f, runner_path + f)
    Spread.spread_calculator_wrapper()
    # destroy everything in the runner_path:
    runner_list = listdir(runner_path)
    for deleted in runner_list:
      remove(runner_path + deleted)

runner()
