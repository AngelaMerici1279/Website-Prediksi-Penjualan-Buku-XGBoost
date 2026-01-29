<?php
defined('BASEPATH') or exit('No direct script access allowed');

class Pegawai extends CI_Controller
{
    public function __construct()
    {
        parent::__construct();
        $this->load->model('Pegawai_Model');
        // Cek apakah user sudah login
        if (!$this->session->userdata('username')) {
            redirect('auth/login');  // Jika belum login, redirect ke halaman login
        }
    }

    public function tambahPegawai()
    {
        $this->load->view('tambahDataPegawai');
    }

    public function insertDataPegawai()
    {

        $role_id = $this->input->post('role_id');
        $username_generate = $this->Pegawai_Model->generateUsername($role_id);
        $data = [
            'nik' => $this->input->post('nik'),
            'nama' => $this->input->post('nama'),
            'jenis_kelamin' => $this->input->post('jenis_kelamin'),
            'alamat' => $this->input->post('alamat'),
            'username' => $username_generate,
            'password' => md5($this->input->post('password')),
            'email' => $this->input->post('email'),
            'role_id' => $this->input->post('role_id'),
            'tanggal_masuk' => $this->input->post('tanggal_masuk'),
            'status' => $this->input->post('status'),
            'gaji' => $this->input->post('gaji')
        ];

        // Upload foto
        if (!empty($_FILES['foto']['name'])) {
            $config['upload_path'] = './uploads/';
            $config['allowed_types'] = 'jpg|jpeg|png';
            $config['max_size'] = 2048;
            $this->load->library('upload', $config);

            if ($this->upload->do_upload('foto')) {
                $data['foto'] = $this->upload->data('file_name');
            } else {
                echo $this->upload->display_errors();
            }
        }

        $this->Pegawai_Model->insertPegawai($data);
        $this->session->set_flashdata('username_generate', 'Data pegawai berhasil ditambahkan. Dengan username: ' . $username_generate);
        redirect('pegawai/tambahdataPegawai');
    }
    public function dataPegawai()
    {
        // if ($role_id) {
        $this->load->model('Pegawai_Model');

        $nama = $this->input->get('nama');
        $divisi = $this->input->get('divisi');

        if (empty($nama) && empty($divisi)) {
            $data['pegawai'] = $this->Pegawai_Model->getAllPegawai();
        } else {
            $data['pegawai'] = $this->Pegawai_Model->getFilterPegawai($nama, $divisi);
        }
        $data['divisi'] = $this->Pegawai_Model->getAllDivisi();

        // $this->load->view('headerdashboard/headerKepegawaian');
        $this->load->view('table', $data);
    }
    public function editPegawai($id_pegawai)
    {
        $data['pegawai'] = $this->Pegawai_Model->getIdPegawai($id_pegawai);
        if (empty($data['pegawai'])) {
            show_404();
        }
        $this->load->view('editPegawai', $data);
    }
    public function updateDataPegawai()
    {
        $id_pegawai = $this->input->post('id_pegawai');
        $data = [
            'nik' => $this->input->post('nik'),
            'nama' => $this->input->post('nama'),
            'jenis_kelamin' => $this->input->post('jenis_kelamin'),
            'alamat' => $this->input->post('alamat'),
            'email' => $this->input->post('email'),
            'role_id' => $this->input->post('role_id'),
            'tanggal_masuk' => $this->input->post('tanggal_masuk'),
            'status' => $this->input->post('status'),
            'gaji' => $this->input->post('gaji')
        ];
        $this->Pegawai_Model->update($id_pegawai, $data);
        $this->session->set_flashdata('success', 'Data pegawai berhasil diperbarui.');
        redirect('Pegawai/dataPegawai');
    }
    public function hapusPegawai($id_pegawai)
    {
        if ($this->session->userdata('role') != '8') {
            $this->session->set_flashdata('error', 'Akses ditolak! Anda tidak memiliki izin untuk menghapus data.');
            redirect('dashboard/dashboardk'); // Arahkan kembali ke dashboard
        }
        $delete = $this->Pegawai_Model->delete($id_pegawai);
        if ($delete) {
            $this->session->set_flashdata('success', 'Data pegawai berhasil dihapus.');
        } else {
            $this->session->set_flashdata('error', 'Gagal menghapus data pegawai.');
        }
        redirect('Pegawai/dataPegawai');
    }
}
