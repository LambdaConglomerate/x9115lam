Main output is in out.txt.

To iterate through models and optimizers:

```
sh run.sh
```

This will launch test.py and write to out.txt. You can also just run test.py but it will append to out.txt. Anything written to console is for troubleshooting.

- model.py contains model class
- Models.py contains models
- mws.py contains Max Walk Sat
- sa.py contains Simmulated Annealing
- state.py contains logger and candidate tracker

