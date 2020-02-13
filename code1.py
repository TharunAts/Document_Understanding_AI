
from google.cloud import vision_v1
from google.cloud.vision_v1 import enums
import io
import six
import os

def sample_batch_annotate_files(file_path,count):
  """
    Perform batch file annotation

    Args:
      file_path Path to local pdf file, e.g. /path/document.pdf
    """

  client = vision_v1.ImageAnnotatorClient()

  # file_path = 'resources/kafka.pdf'

  if isinstance(file_path, six.binary_type):
    file_path = file_path.decode('utf-8')

  # Supported mime_type: application/pdf, image/tiff, image/gif
  mime_type = 'application/pdf'
  with io.open(file_path, 'rb') as f:
    content = f.read()
  input_config = {'mime_type': mime_type, 'content': content}
  type_ = enums.Feature.Type.DOCUMENT_TEXT_DETECTION
  features_element = {'type': type_}
  features = [features_element]

  # The service can process up to 5 pages per document file. Here we specify the
  # first, second, and last page of the document to be processed.
  pages_element = 1
  #pages_element_2 = 2
  #pages_element_3 = -1
  pages = [pages_element]
  requests_element = {'input_config': input_config, 'features': features, 'pages': pages}
  requests = [requests_element]

  response = client.batch_annotate_files(requests)
  filename = "txt1/" + str(count) + ".txt" #location of output txt files
  f = open(filename,'w+')
  for image_response in response.responses[0].responses:
    f.write(image_response.full_text_annotation.text)
  f.close()


def main():
  os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="google.json" #service account details
  path= "/home/Downloads/train/" #location of input files
  l1=os.listdir(path) 
  print(l1)
  count=0
  for i in range(0,len(l1)):
    loc=path + l1[i]
    count=count+1
    sample_batch_annotate_files(loc,count)

  
if __name__== "__main__":
  main()

    
