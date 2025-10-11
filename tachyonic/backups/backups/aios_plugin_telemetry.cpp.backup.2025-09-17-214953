#include "aios_plugin_telemetry.hpp"
#include <mutex>
#include <fstream>
#include <chrono>
#include <filesystem>
#include <atomic>
#include <thread>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#endif

namespace fs = std::filesystem;
namespace aios {

TelemetryBus& TelemetryBus::instance() { static TelemetryBus b; return b; }
void TelemetryBus::register_sink(std::shared_ptr<ITelemetrySink> sink){ sinks_.push_back(std::move(sink)); }
void TelemetryBus::publish(const CoreMetricSample& sample){ for(auto &s: sinks_) s->on_sample(sample); }

static double now_sec(){ using namespace std::chrono; return duration<double>(steady_clock::now().time_since_epoch()).count(); }

JsonFileTelemetrySink::JsonFileTelemetrySink(const std::string& root_dir, size_t flush_every):dir_(root_dir),flush_every_(flush_every){
    fs::create_directories(dir_);
}
void JsonFileTelemetrySink::on_sample(const CoreMetricSample& sample){
    buffer_.push_back(sample); pending_++;
    if(pending_>=flush_every_) flush();
}
JsonFileTelemetrySink::~JsonFileTelemetrySink(){
    try { flush(); } catch(...) {}
}
void JsonFileTelemetrySink::flush(){
    if(buffer_.empty()) return; pending_=0;
    std::string path = dir_ + "/core_metrics.json";
    std::ofstream ofs(path, std::ios::app);
    if(!ofs) return;
    for(auto &s: buffer_){
        ofs << "{\"ts\":"<<s.timestamp_sec<<",\"seq\":"<<s.sequence
            <<",\"cpu\":"<<s.process_cpu_pct<<",\"mem_mb\":"<<s.process_mem_mb
            <<",\"frame_ms\":"<<s.frame_time_ms<<",\"avg_frame_ms\":"<<s.avg_frame_time_ms
            <<"}\n";
    }
    buffer_.clear();
}

struct TelemetrySampler::Impl {
    std::atomic<bool> running{false};
    std::thread th;
    double interval{1.0};
    std::atomic<uint64_t> seq{0};
    std::mutex m;
    double last_frame_ms{-1};
    double avg_frame_ms{-1};
#ifdef _WIN32
    ULONGLONG last_cpu_kernel{0};
    ULONGLONG last_cpu_user{0};
    ULONGLONG last_time{0};
    bool cpu_inited{false};
    double calc_cpu_pct(){
        FILETIME ftCreation, ftExit, ftKernel, ftUser;
        if(!GetProcessTimes(GetCurrentProcess(), &ftCreation, &ftExit, &ftKernel, &ftUser))
            return -1.0;
        ULONGLONG kernel = (((ULONGLONG)ftKernel.dwHighDateTime) << 32) | ftKernel.dwLowDateTime;
        ULONGLONG user = (((ULONGLONG)ftUser.dwHighDateTime) << 32) | ftUser.dwLowDateTime;
        ULONGLONG now = GetTickCount64();
        if(!cpu_inited){ last_cpu_kernel=kernel; last_cpu_user=user; last_time=now; cpu_inited=true; return -1.0; }
        ULONGLONG delta_time_ms = now - last_time; if(delta_time_ms==0) return -1.0;
        ULONGLONG delta_kernel = kernel - last_cpu_kernel;
        ULONGLONG delta_user = user - last_cpu_user;
        last_cpu_kernel = kernel; last_cpu_user = user; last_time = now;
        double cpu_ms = (delta_kernel + delta_user) / 10000.0; // 100ns -> ms
        SYSTEM_INFO si; GetSystemInfo(&si);
        double pct = (cpu_ms / (double)delta_time_ms) * 100.0 / (double)si.dwNumberOfProcessors;
        if(pct < 0) pct = 0; if(pct>100) pct = 100; return pct;
    }
#endif
    void loop(){
        while(running){
            CoreMetricSample sample; sample.timestamp_sec = now_sec(); sample.sequence = seq++;
#ifdef _WIN32
            PROCESS_MEMORY_COUNTERS pmc; if(GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc))){
                sample.process_mem_mb = pmc.WorkingSetSize / (1024.0*1024.0);
            }
#endif
#ifdef _WIN32
            sample.process_cpu_pct = calc_cpu_pct();
#endif
            {
                std::lock_guard<std::mutex> lock(m);
                sample.frame_time_ms = last_frame_ms; sample.avg_frame_time_ms = avg_frame_ms;
            }
            TelemetryBus::instance().publish(sample);
            std::this_thread::sleep_for(std::chrono::duration<double>(interval));
        }
    }
};

TelemetrySampler::TelemetrySampler():impl_(new Impl){}
TelemetrySampler::~TelemetrySampler(){ stop(); }
void TelemetrySampler::start(double interval_sec){
    if(impl_->running) return;
    // Register default JSON sink if none registered yet
    if(true){ // always ensure at least one sink
        static bool sink_registered=false; if(!sink_registered){
            auto sink = std::make_shared<JsonFileTelemetrySink>("runtime_intelligence/logs/core", 1);
            TelemetryBus::instance().register_sink(sink); sink_registered=true;
        }
    }
    impl_->interval=interval_sec; impl_->running=true; impl_->th=std::thread([this]{ impl_->loop();});
}
void TelemetrySampler::stop(){
    if(!impl_->running) return; impl_->running=false; if(impl_->th.joinable()) impl_->th.join();
}
void TelemetrySampler::record_frame(double frame_time_ms){ std::lock_guard<std::mutex> lock(impl_->m); impl_->last_frame_ms=frame_time_ms; if(impl_->avg_frame_ms<0) impl_->avg_frame_ms=frame_time_ms; else impl_->avg_frame_ms = (impl_->avg_frame_ms*0.9)+(frame_time_ms*0.1); }

} // namespace aios
