import pandas as pd
import os
from preprocess_utils.cluster_item import ClusterItem, merge_cluster
from preprocess_utils.house import House
from preprocess_utils.item import Item
from preprocess_utils.card import Card
from preprocess_utils.args import get_args

class Main:
    def __init__(self, args):
        dir_path = args.data_path
        self.house = pd.read_csv(dir_path+"house.csv")
        self.item = pd.read_csv(dir_path+"item.csv")
        self.house_item = pd.read_csv(dir_path+"hi_interaction.csv")
        self.house_card = pd.read_csv(dir_path+"hc_interaction.csv")
        self.card = pd.read_csv(dir_path+"card.csv")
        
        if args.run_test: # 전처리 + 유사도 + 클러스터링의 과정이 오래 걸리기 때문에 test 실행할 수 있게 함.
            
            self.house = self.house[:1000]
            self.item = self.item[:1000]
            self.house_item = self.house_item[:10000]
            self.house_card = self.house_card[:10000]
            self.card = self.card[:10000]
        
        self.preprocessed_house = None
        self.preprocessed_item = None
        self.preprocessed_clusterd_item = None
        self.preprocessed_card = None
    
    def preprocessing(self):
        _house = House(self.house)
        _item = Item(self.item, args)
        _card = Card(self.card, self.house_card)
        
        self.clusterd_item, self.cluster_major_item = merge_cluster(_item.item, self.house_item)
        _cluster_item = ClusterItem(self.cluster_major_item)
        
        self.preprocessed_clusterd_item = _cluster_item.preprocessing()
        self.preprocessed_house = _house.preprocessing()
        self.preprocessed_item = _item.item
        self.preprocessed_card = _card.preprocessing()

    def make_csv(self):
        os.makedirs('output', exist_ok=True)
        output_path = os.path.join('output/')
        # cluster_item은 db에 저장할 때 idx가 필요하므로 index=True로 설정
        self.preprocessed_clusterd_item.to_csv(output_path+"cluster_item.csv")
        self.preprocessed_house.to_csv(output_path+"house.tsv", sep="\t", index=False)
        self.preprocessed_item.to_csv(output_path+"item.tsv", sep="\t", index=False)
        self.preprocessed_card.to_csv(output_path+"card.tsv", sep="\t", index=False)

if __name__ == "__main__":
    args = get_args()
    main = Main(args)
    main.preprocessing()
    main.make_csv()