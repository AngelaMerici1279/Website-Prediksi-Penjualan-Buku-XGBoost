<?php
defined('BASEPATH') or exit('No direct script access allowed');

class Pegawai_Model extends CI_Model
{
    public function __construct()
    {
        parent::__construct();
        $this->load->database();
        $this->table = 'pegawai';
    }
    public function getJumlahPegawai($role_id)
    {
        $this->db->where('role_id', $role_id);
        return $this->db->count_all_results('pegawai');
    }

    public function getAllPegawai()
    {
        $this->db->select('pegawai.*, role.role');
        $this->db->from('pegawai');
        $this->db->join('role', 'role.id = pegawai.role_id');
        return $this->db->get()->result();
    }

    public function dataGrafik()
    {
        $this->db->select('status, count(*) as total');
        $this->db->from('pegawai');
        $this->db->group_by('status');
        return $this->db->get()->result();
    }
    public function get_pegawai_by_role()
    {
        $query = $this->db->query("SELECT role_id, COUNT(*) as jumlah FROM pegawai GROUP BY role_id");
        return $query->result();
    }
    public function dataTanggalMasuk()
    {
        return $this->db->query("
        SELECT DATE_FORMAT(tanggal_masuk, '%Y-%m') as bulan, COUNT(*) as jumlah
        FROM pegawai
        GROUP BY DATE_FORMAT(tanggal_masuk, '%Y-%m')
        ORDER BY bulan ASC
    ")->result();
    }
    public function insertPegawai($data)
    {
        $this->db->insert('pegawai', $data);
    }

    public function generateUsername($role_id)
    {
        // Tentukan prefix berdasarkan role
        if ($role_id == 1) {
            $prefix = '10'; // Kepegawaian
        } elseif ($role_id == 2) {
            $prefix = '20'; // 
        } elseif ($role_id == 3) {
            $prefix = '30'; // Manager
        } elseif ($role_id == 4) {
            $prefix = '40'; // Staff
        } elseif ($role_id == 5) {
            $prefix = '50'; // Staff
        } elseif ($role_id == 6) {
            $prefix = '60'; // Programmer
        } elseif ($role_id == 7) {
            $prefix = '70'; // Percetakan
        } else {
            $prefix = '99'; // Lainnya
        }

        // Ambil username terakhir dengan prefix tersebut
        $this->db->like('username', $prefix, 'after');
        $this->db->order_by('username', 'DESC');
        $last = $this->db->get('pegawai')->row_array();

        if ($last) {
            // Ambil angka terakhir dan tambah 1
            $last_num = (int) substr($last['username'], 2); // ambil bagian belakang setelah prefix
            $new_num = $last_num + 1;
        } else {
            // Kalau belum ada username dengan prefix itu
            $new_num = 1;
        }

        // Format hasilnya: prefix + dua digit (misal: 101, 102, dst)
        return $prefix . str_pad($new_num, 1, '0', STR_PAD_LEFT);
    }
    public function getFilterPegawai($nama = null, $divisi = null)
    {
        $this->db->select('pegawai.*, role.role');
        $this->db->from('pegawai');
        $this->db->join('role', 'role.id = pegawai.role_id');

        if (!empty($nama)) {
            $this->db->like('pegawai.nama', $nama);
        }

        if (!empty($divisi)) {
            $this->db->where('role.role', $divisi);
        }

        return $this->db->get()->result();
    }
    public function getAllDivisi()
    {
        $this->db->select('DISTINCT(role) as role');
        $this->db->from('role');
        $this->db->where('id !=', 8);
        return $this->db->get()->result();
    }
    public function getIdPegawai($id_pegawai)
    {
        return $this->db->get_where('pegawai', ['id_pegawai' => $id_pegawai])->row_array();
    }
    public function update($id, $data)
    {
        $this->db->where('id_pegawai', $id);
        return $this->db->update($this->table, $data);
    }
    public function delete($id)
    {
        $this->db->where(('id_pegawai'), $id);
        return $this->db->delete($this->table);
    }
}
