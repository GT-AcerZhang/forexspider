# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import os,django,sys
sys.path.append('/root/project/news')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewsStatus.settings")
django.setup()

from news.models import News,Trump,Jten
from news.base import AibaseApi
import datetime
import numpy as np
import time



def trump_news():
        ai = AibaseApi()
        cls_task = ai.load()
        data = []
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        obj = Trump.objects.values("content","status").filter(exttime=today,status__isnull=True)
        data = [list(new.values()) for new in obj]
        index = 0
        run_states = cls_task.predict(data=data)
        results = [run_state.run_results for run_state in run_states]
        for batch_result in results:
            batch_result = np.argmax(batch_result, axis=2)[0]
            for result in batch_result:
                Trump.objects.filter(content=data[index][0]).update(status=int(result))
		index += 1

trump_news()

