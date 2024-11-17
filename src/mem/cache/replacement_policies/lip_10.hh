
#ifndef __MEM_CACHE_REPLACEMENT_POLICIES_LIP10_HH__
#define __MEM_CACHE_REPLACEMENT_POLICIES_LIP10_HH__
#include <queue>
#include <functional>

#include "mem/cache/replacement_policies/lru_rp.hh"

namespace gem5
{

struct LIP10RPParams;

namespace replacement_policy
{

class LIP10 : public LRU
{
  public:
    typedef LIP10RPParams Params;
    mutable std::priority_queue<Tick> maxHeap;

    LIP10(const Params &p);
    ~LIP10() = default;

    void invalidate(const std::shared_ptr<ReplacementData>& replacement_data) override;

    void touch(const std::shared_ptr<ReplacementData>& replacement_data) const override;

    void reset(const std::shared_ptr<ReplacementData>& replacement_data) const override;

    ReplaceableEntry* getVictim(const ReplacementCandidates& candidates) const override;
};

} // namespace replacement_policy
} // namespace gem5

#endif // __MEM_CACHE_REPLACEMENT_POLICIES_LIP10_RP_HH__