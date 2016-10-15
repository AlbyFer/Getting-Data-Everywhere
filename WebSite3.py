

dates = ['20161003','20161002','20161001','20160929','20160928','20160927']

def horses_results(days):

    """Connects to the Foo horse races results (just for first and seconds), rides the website and gets the data
    Input: a list of dates as strings in the forms yyyymmdd e.g. 20160926
    Ouput: a pandas data-frame with columns Horse | Position | Day | Time | Track"""

    import requests
    from lxml import html
    import pandas as pd

    init = 'http://www.foo.com'
    col_names = ['Horse', 'Position', 'Day', 'Time', 'Track']
    res_final = pd.DataFrame(columns=col_names)

    def get_horse_results(url_site):
        """ Gets horse results (first and second places) with Names, Times, Places, Position
        Input: a url as string
        Output: a data-frame"""

        page = requests.get(url_site)
        tree = html.fromstring(page.content)

        # --------------------------------------------------------------------------------------------------------- #
        # Getting the horses names

        firsts = tree.xpath('//span[@class="horse pos1"]/text()')
        seconds = tree.xpath('//span[@class="horse pos2"]/text()')


        def get_names(list_horses):
            """"Organise and cleans the racing names into nice list.
                Inputs: a list of names
                Outputs: a list of names as strings """

            holder = []
            for i in range(len(list_horses)):
                names = str(list_horses[i]).split(" ", 1)[1]
                holder.append(names)
            return (holder)

        names_firsts = get_names(firsts)
        names_seconds = get_names(seconds)

        # -------------------------------------------------------------------------------------------------------- #
        # Getting the races times

        hours = tree.xpath('//td[@class="race-time"]/text()')

        def get_times(list_times):
            """"Organize and cleans the racing times into nice list.
            Inputs: a list of times
            Outputs: a list of times as strings """

            iter = len(list_times)
            holder = []
            for i in range(iter):
                time = str(list_times[i]).replace(" ", "")[-5:]
                holder.append(time)
            return (holder)

        race_times = get_times(hours)

        # -------------------------------------------------------------------------------------------------------- #
        # Getting race venues
        venues = tree.xpath('//h2[@class="table-header"]/text()')

        def get_venues(list_venues):
            """"Organize and cleans the racing venues into nice list.
                Inputs: a list of venues
                Outputs: a list of venues as strings """

            holder = []
            for i in range(len(list_venues)):
                places = str(list_venues[i]).replace(" ", "")[1:]
                if places == "":
                    del places
                else:
                    holder.append(places)
            return (holder)

        race_venues = get_venues(venues)

        # -------------------------------------------------------------------------------------------------------- #
        # Getting days of the races

        day = url[-8:]

        # -------------------------------------------------------------------------------------------------------- #
        # Organizing data in a nice data-frame

        # First positions
        col_names = ['Horse', 'Position', 'Day', 'Time', 'Track']
        results = pd.DataFrame(columns=col_names)

        results.Horse = names_firsts
        results.Position = [1] * len(names_firsts)
        results.Day = [day] * len(names_firsts)
        results.Time = race_times

        def fill_track(res_list, places):
            """Fills result data-frame with the racing tracks name
            Inputs: res_list: a list of result with Track and Time columns
            places: a list with the names of the racing venues
            Output: a list"""

            t = 0
            for i in range(1, len(res_list)):
                if res_list.Time[i] > res_list.Time[i - 1]:
                    res_list.Track[i] = places[t]
                else:
                    t += 1
                    res_list.Track[i] = places[t]
            res_list.Track[0] = places[0]
            return (res_list)

        results = fill_track(results, race_venues)

        # Second positions
        res_seconds = pd.DataFrame(columns=col_names)
        res_seconds.Horse = names_seconds
        res_seconds.Position = [2] * len(names_seconds)
        res_seconds.Day = [day] * len(names_seconds)
        res_seconds.Time = race_times
        res_seconds = fill_track(res_seconds, race_venues)

        # Pull it all together
        final = pd.concat([results, res_seconds], ignore_index=True)
        return (final)

    for j in dates:
        url = init + j
        interm = get_horse_results(url)
        res_final = pd.concat([res_final, interm], ignore_index=True)
    return (res_final)

# --------------------------------------------------------------------------------------------------------- #

dataset = horses_results(dates)
dataset.to_csv('/Users/StarShipIV/Documents/Progetti/I_Freakin_Love_Riding_Horses/Races_results')
