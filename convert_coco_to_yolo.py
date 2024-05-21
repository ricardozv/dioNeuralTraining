import os
import json

def convert_coco_to_yolo(coco_json, image_dir, output_dir, class_names):
    # Verifique se o arquivo JSON existe
    abs_path = os.path.abspath(coco_json)
    print(f"Verificando a existência do arquivo: {abs_path}")
    if not os.path.isfile(abs_path):
        print(f"Arquivo de anotações não encontrado: {abs_path}")
        return
    else:
        print(f"Arquivo de anotações encontrado: {abs_path}")

    with open(abs_path) as f:
        data = json.load(f)

    for image in data['images']:
        file_name = image['file_name']
        image_id = image['id']
        width = image['width']
        height = image['height']
        annotations = [a for a in data['annotations'] if a['image_id'] == image_id]

        yolo_annotations = []
        for ann in annotations:
            category_id = ann['category_id']
            if category_id not in class_names:
                continue
            bbox = ann['bbox']
            x, y, w, h = bbox
            x_center = (x + w / 2) / width
            y_center = (y + h / 2) / height
            w /= width
            h /= height
            label_id = class_names.index(category_id)
            yolo_annotations.append(f"{label_id} {x_center} {y_center} {w} {h}\n")

        output_file = os.path.join(output_dir, file_name.replace('.jpg', '.txt'))
        with open(output_file, 'w') as f:
            f.writelines(yolo_annotations)

    print(f"Conversão concluída. Arquivos salvos em {output_dir}")

# Configurações
coco_json = 'C:/Users/ricardo.neto/Downloads/rede/yoloNetwork/annotations/instances_val2017.json'
image_dir = 'C:/Users/ricardo.neto/Downloads/rede/yoloNetwork/val2017'
output_dir = 'C:/Users/ricardo.neto/Downloads/rede/yoloNetwork/yolo_labels'
# Substitua pelos IDs das classes de interesse no COCO
class_names = [1, 2]  # IDs das classes que você deseja usar

# Verificar caminhos antes de continuar
print(f"Verificando o arquivo de anotações em: {coco_json}")
print(f"Diretório de imagens: {image_dir}")
print(f"Diretório de saída: {output_dir}")
print(f"Diretório de trabalho atual: {os.getcwd()}")

# Cria o diretório de saída, se não existir
os.makedirs(output_dir, exist_ok=True)

# Executa a conversão
convert_coco_to_yolo(coco_json, image_dir, output_dir, class_names)
