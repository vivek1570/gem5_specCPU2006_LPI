
#include "mem/cache/replacement_policies/lip_2.hh"

#include <memory>

#include "params/LIP2RP.hh"
#include "sim/cur_tick.hh"

namespace gem5
{

namespace replacement_policy
{

LIP2::LIP2(const Params &p)
    : LRU(p)
{
}
void
LIP2::reset(const std::shared_ptr<ReplacementData>& replacement_data) const
{

    // Set last touch timestamp
    std::static_pointer_cast<LRUReplData>(
        replacement_data)->lastTouchTick = maxHeap.top() + 1;

}

void
LIP2::invalidate(const std::shared_ptr<ReplacementData>& replacement_data)
{
    // Reset last touch timestamp
    std::static_pointer_cast<LRUReplData>(
        replacement_data)->lastTouchTick = Tick(0);

}

void
LIP2::touch(const std::shared_ptr<ReplacementData>& replacement_data) const
{
    // Update last touch timestamp
    std::static_pointer_cast<LRUReplData>(
        replacement_data)->lastTouchTick = curTick();

}

ReplaceableEntry*
LIP2::getVictim(const ReplacementCandidates& candidates) const
{
    // There must be at least one replacement candidate
    assert(candidates.size() > 0);

    while (!maxHeap.empty()) {
    maxHeap.pop();
}

    // Visit all candidates to find victim
    ReplaceableEntry* victim = candidates[0];
    for (const auto& candidate : candidates) {

        auto lru_data = std::static_pointer_cast<LRUReplData>(candidate->replacementData);

        if (std::static_pointer_cast<LRUReplData>(
                    candidate->replacementData)->lastTouchTick <
                std::static_pointer_cast<LRUReplData>(
                    victim->replacementData)->lastTouchTick) {
            victim = candidate;
        }

        if(maxHeap.size()<10)
        {
            maxHeap.push(lru_data->lastTouchTick);
        }
        else{
            if(maxHeap.top()>lru_data->lastTouchTick)
            {
                maxHeap.pop();
                maxHeap.push(lru_data->lastTouchTick);
            }
        }
        

    }

    return victim;
}

} // namespace replacement_policy
} // namespace gem5


