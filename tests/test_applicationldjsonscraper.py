from eventscraper.scrapers.applicationldjsonscraper import ApplicationLdJsonScraper


def test_convert_numbers_to_strings_in_json():
    replaced = ApplicationLdJsonScraper.convert_numbers_to_strings_in_json('''
    {
        "upsi": 01234,
        "dupsi": 
            1234 ,
        "notme": "333",
        "nope": "3:33",
        "yes" :   444
    }
    ''')

    assert '''
    {
        "upsi": "01234",
        "dupsi": 
            "1234" ,
        "notme": "333",
        "nope": "3:33",
        "yes" :   "444"
    }
    ''' == replaced

def test_clean_invalid_json():
    cleaned = ApplicationLdJsonScraper.clean_invalid_json('''
    {
        "some": "where",
        "over": "the rainbow",
        
        <!----><!---->  }
    ''')

    assert '''
    {
        "some": "where",
        "over": "the rainbow"}
    ''' == cleaned


def test_drop_invalid_lines():
    cleaned = ApplicationLdJsonScraper.drop_invalid_lines('''
    {
        "some": "where",
        "over": "the "rainbow"",
        "way": "up high"
    }
    ''')

    assert '''
    {
        "some": "where",
        "way": "up high"
    }
    ''' == cleaned


def test_remove_superfluous_commata():
    cleaned = ApplicationLdJsonScraper.remove_superfluous_commata('''
    {
        "some": "where",
        "over": {
            "the": "rainbow",
        },
    }
    ''')

    assert '''
    {
        "some": "where",
        "over": {
            "the": "rainbow" } }
    ''' == cleaned
