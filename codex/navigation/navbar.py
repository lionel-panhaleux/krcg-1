def getNavigation ():
	return {
		'Home':['index'],

		'Strategy':['Strategy',
			{'Index':['Fundamentals','Combat','Bloat','Deck building','Archetypes','Table Talk']},
			{'Decks guides':['Den of Fiends','Libertine Ball','Pact with Nephandi','Parliament of Shadows']}
		],

		'Archetypes':['Archetypes',
			{'Index':['AAA','Akunanse Wall','Amaravati Politics','Anti ventrue Grinder','Baltimore Purge',
				  'Bima Dominate','Black Hand','Cats','Council of Doom','Cybelotron','Daughters Politics',
				  'Death Star','Dmitri\'s Big Band','Emerald Legion','Euro Brujah','Girls Will Find Inner Circle',
				  'Goratrix High Tower','Guruhi Rush','Hunters','Ishtarri Politics','Jost Powerbleed',
				  'Khazar\'s Diary','Kiasyd Stealth & Bleed','Lasombra Nocturn','Lutz Politics','Madness Reversal',
				  'Mind Rape','Mistress','Nananimalism','Nephandii','Nosferatu Royalty','Rachel Madness',
				  'Ravnos Clown Car','Renegade Assault','Saulot & Friends','Scout','Shambling Hordes',
				  'Spirit Marionette','Stanislava','Team Jacob','The Bleeding Vignes','The Dark Side of Politics',
				  'The unnamed','Tupdogs','Tzimisce Toolbox','Tzimisce Wall','Ventrue Royalty','War Chantry',
				  'War Ghouls','Weenie AUS','Weenie DEM','Weenie DOM']}
		],

		'Best Cards':['Best Cards',
			{'Generic':['Master','Political action','No discipline','Animalism','Auspex','Celerity',
					'Dominate','Fortitude','Necromancy','Obfuscate','Potence','Presence']},
			{'Sects':['Anarch','Camarilla','Laibon','Sabbat']},
			{'Clans':['Ahrimanes','Akunanse','Assamite','Baali','Brujah','Caitiff','Daughters of Cacophony',
				  'Followers of Set','Gangrel','Giovanni','Guruhi','Harbingers of Skulls',
				  'Imbued','Ishtarri','Kiasyd','Lasombra','Malkavian','Nosferatu','Ravnos',
				  'Salubri','Toreador','Tremere','True Brujah','Tzimisce','Ventrue']}
		],

		'Deck Search':['Deck Search'],

		'Card Search':['Card Search']
	}

def getHelper (navigation):
	navigation_helper = {}

	for key, sections in navigation.items():
	    for item in sections:
	    	if isinstance(item, str):
	    		top = item
	    		continue
	    	for section, pages in item.items():
	    		for index, page in enumerate(pages):
	    			navigation_helper[page] = {
	    				"top": top,
	    				"previous": pages[index - 1] if index > 0 else None,
	    				"next": pages[index + 1] if index < len(pages) - 1 else None,
	    			}
	return navigation_helper

def getNavLinks (category, page):
	# If root file of a category
	if 'index_' in page:
		page = page.replace('index_','').capitalize()
	#
	navigation = getNavigation()
	if category in navigation.keys():
    	print navigation[category]
		helper = getHelper(navigation[category])
		return helper[page]
	return ""
