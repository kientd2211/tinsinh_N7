import os
import requests
import torch
import numpy as np
import matplotlib.pyplot as plt
from Bio.PDB import PDBParser, Superimposer

# 1. Cấu hình đường dẫn
SEQUENCE = "TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN" # Crambin
EIGEN_DIR = "./pretrained_model/demo.csv.ep7.num5.step0.5.alpha0.beta1.elbo0.2"
EIGEN_FILES = [f"crambin.{i}.pdb" for i in range(5)]

def get_esmfold_pdb(seq):
    print("--> Đang lấy cấu trúc từ API ESMFold (Meta)...")
    url = "https://api.esmatlas.com/foldSequence/v1/pdb/"
    response = requests.post(url, data=seq)
    return response.text

def calculate_rmsd(pdb_str_ref, pdb_path_sample):
    parser = PDBParser(QUIET=True)
    
    # Load Ref (ESMFold) từ chuỗi PDB
    import io
    ref_structure = parser.get_structure("ref", io.StringIO(pdb_str_ref))
    
    # Load Sample (EigenFold) từ file
    sample_structure = parser.get_structure("sample", pdb_path_sample)
    
    # Lấy các nguyên tử CA (Carbon alpha)
    ref_atoms = [a for a in ref_structure.get_atoms() if a.get_name() == 'CA']
    sample_atoms = [a for a in sample_structure.get_atoms() if a.get_name() == 'CA']
    
    # Cắt ngắn nếu lệch độ dài (đảm bảo so sánh đúng)
    min_len = min(len(ref_atoms), len(sample_atoms))
    ref_atoms = ref_atoms[:min_len]
    sample_atoms = sample_atoms[:min_len]
    
    super_imposer = Superimposer()
    super_imposer.set_atoms(ref_atoms, sample_atoms)
    return super_imposer.rms

def main():
    print("=== HỆ THỐNG SO SÁNH CẤU TRÚC PROTEIN ===")
    
    # Lấy dữ liệu ESMFold
    esm_pdb = get_esmfold_pdb(SEQUENCE)
    with open("esmfold_result.pdb", "w") as f:
        f.write(esm_pdb)
    
    rmsds = []
    print("\n[KẾT QUẢ SO SÁNH TRÊN CONSOLE]")
    print("-" * 45)
    print(f"{'Mẫu thử':<20} | {'RMSD vs ESMFold (Å)':<20}")
    print("-" * 45)
    
    for i, f_name in enumerate(EIGEN_FILES):
        path = os.path.join(EIGEN_DIR, f_name)
        if os.path.exists(path):
            rms = calculate_rmsd(esm_pdb, path)
            rmsds.append(rms)
            print(f"EigenFold Sample {i:<2} | {rms:>12.3f} Å")
    
    # In thống kê
    avg_rms = np.mean(rmsds)
    std_rms = np.std(rmsds)
    print("-" * 45)
    print(f"TRUNG BÌNH RMSD: {avg_rms:.3f} Å (±{std_rms:.3f})")
    print("-" * 45)
    print("\nGIẢI THÍCH: RMSD càng thấp (< 2.0Å) thì càng giống ESMFold.")
    print("Độ lệch (±) thể hiện tính đa dạng (Diversity) của EigenFold.")

    # Vẽ biểu đồ
    plt.figure(figsize=(8, 5))
    plt.bar([f"S.{i}" for i in range(len(rmsds))], sorted(rmsds), color='skyblue', edgecolor='navy')
    plt.axhline(y=avg_rms, color='red', linestyle='--', label=f'Trung bình: {avg_rms:.2f}Å')
    plt.ylabel("RMSD (Å) - Thấp hơn là giống ESMFold hơn")
    plt.title("So sánh sai lệch giữa các mẫu EigenFold so với ESMFold")
    plt.legend()
    plt.savefig("comparison_chart.png")
    print("\n--> Đã lưu biểu đồ so sánh tại: comparison_chart.png")

if __name__ == "__main__":
    main()