import anime.accept_job_change
import anime.jobs
import anime.congratulations
import anime.secret_quest
import anime.levelup
import anime.instance_dungeon
import anime.bars

TEST_VAL="job5"
SIZE_VAL="default"
fin=[]
def runner_start(canvas=None, window=None):
    if SIZE_VAL=="default":
        if TEST_VAL=="accept_job_change": fin=anime.accept_job_change.main(canvas)
        elif TEST_VAL=="job0": fin=anime.jobs.job0(canvas,window)
        elif TEST_VAL=="job1": fin=anime.jobs.job1(canvas,window)
        elif TEST_VAL=="job2": fin=anime.jobs.job2(canvas,window)
        elif TEST_VAL=="job3": fin=anime.jobs.job3(canvas,window)
        elif TEST_VAL=="job4": fin=anime.jobs.job4(canvas,window)
        elif TEST_VAL=="job5": fin=anime.jobs.job5(canvas,window)
        elif TEST_VAL=="congrats": fin=anime.congratulations.main(canvas)
        elif TEST_VAL=="first_secret_quest": fin=anime.secret_quest.main(canvas, window) #! NOT WORKING
    
    elif SIZE_VAL=="small":
        if TEST_VAL=="level_up": fin=anime.levelup.main(canvas)
        elif TEST_VAL=="instance": fin=anime.instance_dungeon.main(canvas, window)
        elif TEST_VAL=="hp_bar": fin=anime.bars.hp_bar(canvas, window)
    
    print(len(fin))
    return fin