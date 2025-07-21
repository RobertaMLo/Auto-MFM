run_optim_CMA_ES_parallel.sh : pipeline to run a optimization code based on CMA_ES algorithm. Goal: estimate alpha grc, goc, mli, pc by minnimizing the discrepancy between slope and mae of SNN simulations (_3.csv files) for 4,40,80 Hz. It calls trial_optim_3freq.py

run_optim_NSGA2_parallel.sh : same scope as above, but maybe more sophisticate. It calls multi_obj_mfm_3freq.py 
