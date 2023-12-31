from api.models import CodeForcesGym
from api.services.site_service import SiteService
from datetime import datetime
from pytz import timezone

UTC_FORMAT = "%Y-%m-%d %H:%M:%S:%f"
SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR   = SECONDS_IN_MINUTE * 60
SECONDS_IN_DAY    = SECONDS_IN_HOUR * 24 


CONTESTS_URL = 'https://codeforces.com/api/contest.list?gym=true'
class CodeforcesGymService(SiteService):
    def extract_contests(self,data):
        return( data['result'])


    def create_contests(self,contests):
        for contest in contests:
            #print(contest)
            # or contest['phase']=="FINISHED"
            if contest['phase']=="BEFORE" or contest['phase']=="CODING":
                contest_info=CodeforcesGymService().extract_contest_info(contest)
                data=CodeForcesGym(name=contest_info["name"],
                              url =contest_info["url"],
                              duration = contest_info["duration"],
                              start_time =contest_info["start_time"],
                               end_time =contest_info["end_time"],
                              status =contest_info["status"],
                              in_24_hours =contest_info["in_24_hours"]


                              )
                data.save()

    def unixToUtc(self,unixTimeStamp) -> str:
        #time_stamp = 1668306600 (unix time stamp) example
        original_time = datetime.fromtimestamp(unixTimeStamp)
        utc_time = original_time.astimezone(timezone('UTC'))
        start_time = utc_time.strftime(UTC_FORMAT)
        return start_time #returns string

    
    def extract_contest_info(self,contest):

        contest_info = {}
        contest_info["name"] = contest['name']
        contest_info["url"] = f"https://codeforces.com/gymRegistration/{contest['id']}"
        contest_info["duration"] = contest['durationSeconds']
        #contest_info["difficulty"] = contest['difficulty']
        contest_info["status"] = contest['phase']
        
        try:
            a = contest['startTimeSeconds']
        except KeyError as e:
            a = False
            
        if (a == False):
            contest_info["start_time"] = '-'
            contest_info["end_time"] = '-'
            in_24_hours = 'No'
        else:
            contest_info["start_time"] = CodeforcesGymService().unixToUtc(contest['startTimeSeconds'])
            contest_info["end_time"] = CodeforcesGymService().unixToUtc(contest['startTimeSeconds']+contest_info["duration"])
            contest_info["in_24_hours"] = CodeforcesGymService().in_24_hours(contest_info["start_time"],contest_info["status"])
        return contest_info



    def update_contests(self):
        CodeForcesGym.objects.all().delete()
        #1.get the html
        response=CodeforcesGymService().make_request(CONTESTS_URL)

        htmlContent=response.content
        #html has been parsed
        data = CodeforcesGymService().create_data_object(htmlContent)

        contests = CodeforcesGymService().extract_contests(data)
        #print(contests)
        CodeforcesGymService().create_contests(contests)
        # for i in contests:
        #     print(i)
        #print(contests)    

# CodeforcesGymService().update_contests()    



