class Course:

    def date_split(date):
        date_list = []
        date_len = len(date)
        if date_len == 6:
            date_list = [date[0:1], date[4:5]]
            date_set(date_list)
        else if date_len == 10:
            date_list = [date[0:1], date[4:5], date[8:9]]
            date_set(date_list)
        else if date_len == 2:
            date_list = [date]
        else
        print("Ill formated date string")

    def date_set(date_list):
        days = [Mo, Tu, We, Th, Fr]
        for date in date_list:
            for day in days:
                if date == day:

    def
