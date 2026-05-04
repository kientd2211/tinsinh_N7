🛠 Hướng dẫn cài đặt (Dành cho Windows)
Dự án đã được tùy chỉnh để chạy ổn định trên Windows (CPU) mà không gặp lỗi thư viện C++ hay lỗi đường dẫn hệ thống.

1. Khởi tạo môi trường ảo
Mở Terminal tại thư mục dự án:

python -m venv env
.\env\Scripts\activate
2. Cài đặt thư viện (Theo thứ tự bắt buộc)
Để tránh lỗi "DLL Hell" và xung đột phiên bản trên Windows, vui lòng cài đặt chính xác theo thứ tự sau:

PowerShell
# 1. Cài đặt PyTorch chuẩn 1.13.1 cho CPU
pip install torch==1.13.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# 2. Cài đặt bộ công cụ PyTorch Geometric (bản vá lỗi Windows)
pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric==2.2.0 -f https://data.pyg.org/whl/torch-1.13.1+cpu.html

# 3. Cài đặt các thư viện bổ trợ khác
pip install e3nn==0.5.1 numpy==1.26.4 requests wandb biopython matplotlib pandas tqdm

3. Tải trọng số mô hình (Weights)
Do giới hạn dung lượng GitHub, các file trọng số không được push lên. Bạn cần tải file sau và đặt vào thư mục gốc:

[release1.pt.  ](https://helixon.s3.amazonaws.com/release1.pt)

Cấu trúc thư mục mô hình cần có file args.yaml đi kèm trong pretrained_model/.

4. Clone OmegaFold
git clone https://github.com/bjing2016/OmegaFold
pip install --no-deps -e OmegaFold

🚀 Cách chạy dự án
1. Dự đoán cấu trúc (Inference)
Sử dụng lệnh sau để sinh mẫu cấu trúc cho protein trong file demo.csv:

PowerShell
python inference.py --model_dir ./pretrained_model --ckpt release1.pt --embeddings_dir ./embeddings --embeddings_key name --num_samples 5 --splits demo.csv
Kết quả (file .pdb) sẽ được lưu tại thư mục con bên trong pretrained_model/.