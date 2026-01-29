<?php
defined('BASEPATH') or exit('No direct script access allowed');

class PenjualanModel extends CI_Model
{
    public function __construct()
    {
        parent::__construct();
        $this->load->database();
        $this->table = 'data';
    }
    // Ambil detail data untuk tabel berdasarkan tahun
    public function get_detail_by_year($tahun)
    {
        $this->db->select('kategoriNama, gudangNama, propNama, tahunBulan, jumEks');
        // Pastikan nama tabel ini benar (di sini saya pakai 'data' sesuai kode Anda)
        $this->db->from('data');
        $this->db->like('tahunBulan', $tahun, 'after');
        $query = $this->db->get();
        return $query->result_array();
    }
    public function get_summary_stats_db()
    {
        // Kueri: Ambil 4 karakter pertama tahunBulan (Tahun), jumlahkan jumEks, kelompokkan per Tahun
        $this->db->select('LEFT(tahunBulan, 4) as tahun, SUM(jumEks) as total');
        $this->db->from('data'); // Sesuai dengan nama tabel Anda
        $this->db->group_by('tahun');
        $query = $this->db->get();

        $result = $query->result();
        $stats = [];

        // Format data agar menjadi array key-value: ['2020' => 500, '2021' => 700]
        foreach ($result as $row) {
            $stats[$row->tahun] = (int)$row->total;
        }

        return $stats;
    }
}
