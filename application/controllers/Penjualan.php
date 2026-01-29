<?php
defined('BASEPATH') or exit('No direct script access allowed');

class penjualan extends CI_Controller
{
    public function __construct()
    {
        parent::__construct();
        // Load model di constructor
        $this->load->model('PenjualanModel');
    }
    // Endpoint untuk detail (tabel)
    public function getDetailByYear($tahun)
    {
        $data = $this->PenjualanModel->get_detail_by_year($tahun);
        header('Content-Type: application/json');
        echo json_encode($data);
    }
    public function getSummaryStats()
    {
        // Ambil data langsung dari database melalui Model
        $data = $this->PenjualanModel->get_summary_stats_db();

        // Jika data kosong, kirim array kosong agar JS tidak error
        if (empty($data)) {
            $data = [
                '2020' => 0,
                '2021' => 0,
                '2022' => 0,
                '2023' => 0,
                '2024' => 0
            ];
        }

        // Kembalikan JSON ke View
        header('Content-Type: application/json');
        echo json_encode($data);
    }

    public function Prediksipenjualan()
    {
        $ch = curl_init('http://127.0.0.1:5000/dropdown');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);
        curl_close($ch);

        $result = json_decode($response, true);

        $data['kategori'] = $result['kategori'];
        $data['provinsi'] = $result['provinsi'];
        $data['gudang'] = $result['gudang'];

        $this->load->view('prediksi/prediksiPenjualan', $data);
    }

    public function hitungPrediksi()
    {
        // 1. Ambil input dari AJAX (JSON)
        $input = json_decode($this->input->raw_input_stream, true);

        // 2. Kirim ke Flask
        $ch = curl_init('http://127.0.0.1:5000/predict');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($input));
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);

        $response = curl_exec($ch);
        curl_close($ch);

        // 3. Kirim balik ke JavaScript View tanpa mengubah strukturnya
        // Di sinilah data 'mae_spesifik' dari Flask akan ikut terkirim ke View
        echo $response;
    }

    public function simpanHasil()
    {
        // 1. Cek Data Masuk
        $raw_input = file_get_contents('php://input');
        $input = json_decode($raw_input, true);

        if (!$input) {
            // Error: Data JSON tidak terkirim/rusak
            http_response_code(400);
            echo json_encode(['status' => 'error', 'msg' => 'Tidak ada data JSON yang diterima controller']);
            return;
        }

        // 2. Load Database (Jaga-jaga kalau belum di-autoload)
        $this->load->database();

        // 3. Siapkan Data Header
        // Cek session, kalau kosong pakai default 1 (Admin)
        $id_pegawai = $this->session->userdata('id_pegawai') ? $this->session->userdata('id_pegawai') : 1;

        $data_header = [
            'id_pegawai'   => $id_pegawai,
            'tgl_prediksi' => date('Y-m-d H:i:s'),
            'kategori'     => $input['kategori'],
            'provinsi'     => $input['provinsi'],
            'gudang'       => $input['gudang']
        ];

        // 4. Insert Header & Cek Error
        if (!$this->db->insert('tb_riwayat_prediksi', $data_header)) {
            // Error Database Header
            $error = $this->db->error();
            http_response_code(500);
            echo json_encode(['status' => 'error', 'msg' => 'Gagal Insert Header: ' . $error['message']]);
            return;
        }

        $id_header_baru = $this->db->insert_id();

        // 5. Siapkan Data Detail
        $data_detail = [];
        if (isset($input['hasil_loop']) && is_array($input['hasil_loop'])) {
            foreach ($input['hasil_loop'] as $row) {
                $data_detail[] = [
                    'id_prediksi' => $id_header_baru,
                    'bulan'       => $row['bulan'],
                    'jumlah'      => $row['eksemplar']
                ];
            }
        } else {
            http_response_code(400);
            echo json_encode(['status' => 'error', 'msg' => 'Data hasil_loop kosong atau format salah.']);
            return;
        }

        // 6. Insert Detail & Cek Error
        if (!empty($data_detail)) {
            if ($this->db->insert_batch('tb_detail_prediksi', $data_detail)) {
                echo json_encode(['status' => 'success', 'msg' => 'Data berhasil disimpan!']);
            } else {
                // Error Database Detail
                $error = $this->db->error();
                http_response_code(500);
                echo json_encode(['status' => 'error', 'msg' => 'Gagal Insert Detail: ' . $error['message']]);
            }
        } else {
            echo json_encode(['status' => 'warning', 'msg' => 'Tidak ada detail yang disimpan.']);
        }
    }
}
