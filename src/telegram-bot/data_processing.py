import pandas as pd

def clean_data(jobs_all):
  jobs_all.reset_index(inplace = True)
  
  job_highlights = jobs_all['job_highlights'].to_dict()
  
  extracted_highlights = {}
  for k,v in job_highlights.items():
    items_list = [item_dict['items'] for item_dict in v][0][0]
    extracted_highlights[k] = items_list
    
  descs = []
  for k,desc in extracted_highlights.items():
    descs.append(desc)
    
    
  related_links = jobs_all['related_links'].to_dict()
  extracted_links = {}
  for k,v in related_links.items():
    items_list = [item_dict['link'] for item_dict in v][-1]
    extracted_links[k] = items_list
  links = []
  for k,link in extracted_links.items():
    links.append(link)
    
  data = {
    'description': descs,
    'link': links
  }
  extracted_df = pd.DataFrame(data)
  
  # dropping columns
  jobs_all = jobs_all[['title', 'company_name', 'location', 'via', 'job_id','posted_at', 'schedule_type', 'date_time', 'search_term',
        'search_location']]

  jobs_df = pd.concat([jobs_all,extracted_df], axis = 1)
  
  return jobs_df