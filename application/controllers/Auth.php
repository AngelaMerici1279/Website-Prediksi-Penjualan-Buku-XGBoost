<?php

use SebastianBergmann\Environment\Console;

defined('BASEPATH') or exit('No direct script access allowed');

class Auth extends CI_Controller
{

    public function __construct()
    {
        parent::__construct();
        $this->load->library('session');
        $this->load->library('form_validation');
        $this->load->model('Auth_model');
    }
    public function index()
    {
        $this->load->view('templates/auth_header');
        $this->load->view('auth/login');
        $this->load->view('templates/auth_footer');
    }
    // Proses login
    public function login_process()
    {
        $username = $this->input->post('username');
        $password = $this->input->post('password');
        // Panggil model untuk memverifikasi login
        $user = $this->Auth_model->verifyLogin($username, $password);

        if ($user) {
            // Jika login sukses, buat session
            $this->session->set_userdata('username', $user['username']);
            $this->session->set_userdata('nama', $user['nama']);
            // echo $user['nama'];
            $this->session->set_userdata('role', $user['role_id']); // Simpan role ke session

            // Arahkan ke dashboard berdasarkan role
            if ($user['role_id'] == '1' || $user['role_id'] == '8') {
                redirect('dashboard/Kepegawaian'); // Redirect ke halaman kepegawaian
            } elseif ($user['role_id'] == '2') {
                redirect('dashboard/Penjualan'); // Redirect ke halaman penjualan
            }
        } else {
            $this->session->set_flashdata('error', 'Username atau password salah!');
            redirect('auth/login');
        }
    }

    // Logout
    public function logout()
    {
        $this->session->sess_destroy();  // Hapus session
        redirect('auth/login');  // Redirect ke halaman login setelah logout
    }

    public function registration()
    {
        $this->load->view('templates/auth_header');
        $this->load->view('auth/registration');
        $this->load->view('templates/auth_footer');
    }
}
