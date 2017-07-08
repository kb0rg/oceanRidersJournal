

## text display options for ratings
ENTRY_DETAIL_OPTS = {
    'wave_challenge': {
        1 : 'easy',
        2 : 'easy plus a little juice',
        3 : 'just right/ neutral',
        4 : 'little bit of a stretch',
        5 : 'super intense',
        },

    'wave_fun': {
        1 : 'meh',
        2 : 'kind of alright',
        3 : 'just right/ neutral',
        4 : 'fun!',
        5 : 'epic!',
        },

    'crowd_den': {
        1 : 'just me and the marine mammals',
        2 : 'lots of space',
        3 : 'manageable lineup',
        4 : 'kind of crowded',
        5 : 'human obstacle course',
        },

    'crowd_vibe': {
        1 : 'grrrr',
        2 : 'arrgh',
        3 : 'meh',
        4 : 'alright!',
        5 : 'wooooo!',
        },

    'overall_fun': {
        1 : 'should\'ve gone for a bike ride',
        2 : 'not too bad',
        3 : 'alright/ neutral',
        4 : 'pretty fun',
        5 : 'made my day!',
        },
}

def format_for_chart(entry):
    """
    format needed by highcharts:
    [{
        "data": [[x, y, z, interval], [x, y, z, interval]],
        "name": "data_name_for_display"
        },
    ]

    name = name of beach,
    x = swell height,
    y = swell direction in degrees,
    z = bubble_size = overall user rating,
    interval = swell period
    """

    ## clean ratings data (convert any "None" -> 0)
    bubble_size = entry.rate_overall_fun
    if not isinstance(bubble_size, int):
        bubble_size = 0

    return {
        "x": entry.swell1_ht,
        "y": entry.swell1_dir_deg_global,
        "z": bubble_size,
        "interval": entry.swell1_per,
        }
