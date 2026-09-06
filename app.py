import streamlit as st

from memory_ai import analyze_memories

from database import (
    init_db,
    save_memory,
    save_parent,
    get_all_memories,
    get_parents
)

from hash_utils import make_memory_hash

from blockchain import (
    is_connected,
    get_blockchain_memory,
    verify_blockchain_memory
)


st.set_page_config(
    page_title="MemoryGit",
    page_icon="🧠",
    layout="wide"
)


init_db()


if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "approved_memory" not in st.session_state:
    st.session_state.approved_memory = None

if "approved_hash" not in st.session_state:
    st.session_state.approved_hash = None

if "rejected" not in st.session_state:
    st.session_state.rejected = False

if "chatgpt_memory_id" not in st.session_state:
    st.session_state.chatgpt_memory_id = None

if "claude_memory_id" not in st.session_state:
    st.session_state.claude_memory_id = None

if "canonical_memory_id" not in st.session_state:
    st.session_state.canonical_memory_id = None


st.title("🧠 MemoryGit")

st.write(
    "여러 AI에서 서로 다르게 형성된 사용자 기억을 "
    "비교하고 병합하며, 최종 기억은 사용자가 직접 승인합니다."
)


tab1, tab2, tab3 = st.tabs([
    "기억 비교 및 병합",
    "Memory History",
    "블록체인 검증"
])


with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ChatGPT Branch")

        chatgpt_memory = st.text_area(
            "ChatGPT에서 형성된 기억을 입력하세요",
            height=180,
            placeholder="예: 사용자는 블록체인 보안 분야에 관심이 있다."
        )

    with col2:
        st.subheader("Claude Branch")

        claude_memory = st.text_area(
            "Claude에서 형성된 기억을 입력하세요",
            height=180,
            placeholder="예: 사용자는 AI 보안 연구에도 관심이 있다."
        )

    st.divider()

    if st.button(
        "🔍 기억 비교하기",
        type="primary",
        use_container_width=True
    ):

        if not chatgpt_memory.strip() or not claude_memory.strip():

            st.warning(
                "ChatGPT와 Claude 기억을 모두 입력해주세요."
            )

        else:

            try:

                with st.spinner(
                    "로컬 AI가 두 기억의 의미를 비교하고 있습니다..."
                ):

                    result = analyze_memories(
                        chatgpt_memory,
                        claude_memory
                    )

                    chatgpt_id = save_memory(
                        "ChatGPT",
                        chatgpt_memory,
                        "branch"
                    )

                    claude_id = save_memory(
                        "Claude",
                        claude_memory,
                        "branch"
                    )

                    st.session_state.chatgpt_memory_id = chatgpt_id
                    st.session_state.claude_memory_id = claude_id

                    st.session_state.analysis = result
                    st.session_state.approved_memory = None
                    st.session_state.approved_hash = None
                    st.session_state.rejected = False
                    st.session_state.canonical_memory_id = None

            except Exception as e:

                st.error(
                    f"AI 분석 중 오류가 발생했습니다.\n\n{e}"
                )

    if st.session_state.analysis:

        result = st.session_state.analysis

        st.divider()

        st.header("🧠 Semantic Diff 결과")

        relation = result.get(
            "relation",
            "UNKNOWN"
        )

        relation_korean = {
            "SAME": "같은 기억",
            "COMPLEMENTARY": "서로 보완되는 기억",
            "CONFLICT": "충돌하는 기억",
            "UPDATED": "변경된 기억",
            "INDEPENDENT": "서로 독립적인 기억"
        }

        st.subheader(
            f"관계: {relation_korean.get(relation, relation)}"
        )

        st.info(
            result.get(
                "reason",
                "분석 결과가 없습니다."
            )
        )

        merge_proposal = result.get(
            "merge_proposal",
            ""
        )

        if merge_proposal:

            st.divider()

            st.header("🔀 AI 병합 제안")

            edited_memory = st.text_area(
                "병합될 기억",
                value=merge_proposal,
                height=120
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ 승인",
                    use_container_width=True
                ):

                    memory_hash = make_memory_hash(
                        edited_memory
                    )

                    canonical_id = save_memory(
                        "Canonical",
                        edited_memory,
                        "approved",
                        memory_hash
                    )

                    save_parent(
                        canonical_id,
                        st.session_state.chatgpt_memory_id
                    )

                    save_parent(
                        canonical_id,
                        st.session_state.claude_memory_id
                    )

                    st.session_state.approved_memory = edited_memory
                    st.session_state.approved_hash = memory_hash
                    st.session_state.canonical_memory_id = canonical_id
                    st.session_state.rejected = False

            with col2:

                if st.button(
                    "❌ 거절",
                    use_container_width=True
                ):

                    st.session_state.approved_memory = None
                    st.session_state.approved_hash = None
                    st.session_state.rejected = True
                    st.session_state.canonical_memory_id = None

        else:

            st.warning(
                "두 기억은 자동 병합하기 어렵습니다."
            )

    if st.session_state.approved_memory:

        st.divider()

        st.header("✅ Canonical Memory")

        st.success(
            st.session_state.approved_memory
        )

        st.write(
            f"Memory ID: {st.session_state.canonical_memory_id}"
        )

        st.subheader("🔐 SHA-256 Hash")

        st.code(
            st.session_state.approved_hash
        )

        st.info(
            "이 Memory ID와 Hash를 Remix의 registerMemory 함수에 등록하세요."
        )

    if st.session_state.rejected:

        st.divider()

        st.error(
            "병합 제안이 사용자에 의해 거절되었습니다."
        )


with tab2:

    st.header("📜 Memory History")

    memories = get_all_memories()

    if not memories:

        st.info(
            "아직 저장된 기억이 없습니다."
        )

    else:

        for memory in memories:

            memory_id = memory[0]
            branch = memory[1]
            content = memory[2]
            status = memory[3]
            memory_hash = memory[4]
            created_at = memory[5]

            with st.expander(
                f"{memory_id} | {branch} | {status}"
            ):

                st.write(content)

                st.write(
                    f"생성 시간: {created_at}"
                )

                if memory_hash:

                    st.write("SHA-256 Hash")

                    st.code(
                        memory_hash
                    )

                parents = get_parents(
                    memory_id
                )

                if parents:

                    st.write(
                        "부모 기억:"
                    )

                    for parent in parents:

                        st.write(
                            f"- {parent}"
                        )


with tab3:

    st.header("⛓️ Blockchain Verification")

    if is_connected():

        st.success(
            "Ethereum Sepolia 연결 성공"
        )

    else:

        st.error(
            "Sepolia RPC 연결 실패"
        )

    memory_id_input = st.text_input(
        "검증할 Memory ID",
        placeholder="예: M009"
    )

    memory_hash_input = st.text_input(
        "검증할 SHA-256 Hash",
        placeholder="Memory History에 저장된 Hash를 붙여넣으세요"
    )

    if st.button(
        "⛓️ 블록체인 검증하기",
        use_container_width=True
    ):

        if not memory_id_input.strip():

            st.warning(
                "Memory ID를 입력해주세요."
            )

        elif not memory_hash_input.strip():

            st.warning(
                "SHA-256 Hash를 입력해주세요."
            )

        else:

            try:

                with st.spinner(
                    "Sepolia 블록체인에서 기억을 확인하고 있습니다..."
                ):

                    blockchain_data = get_blockchain_memory(
                        memory_id_input
                    )

                    verified = verify_blockchain_memory(
                        memory_id_input,
                        memory_hash_input
                    )

                st.divider()

                st.subheader(
                    "블록체인 저장 정보"
                )

                st.write(
                    "Memory ID"
                )

                st.code(
                    memory_id_input
                )

                st.write(
                    "Blockchain Hash"
                )

                st.code(
                    blockchain_data["memory_hash"]
                )

                st.write(
                    "Approved By"
                )

                st.code(
                    blockchain_data["approved_by"]
                )

                st.write(
                    "Timestamp"
                )

                st.code(
                    str(blockchain_data["timestamp"])
                )

                st.divider()

                if verified:

                    st.success(
                        "✅ 검증 성공: 승인된 기억의 Hash와 블록체인 기록이 일치합니다."
                    )

                else:

                    st.error(
                        "❌ 검증 실패: 입력한 Hash와 블록체인 기록이 일치하지 않습니다."
                    )

            except Exception as e:

                st.error(
                    f"블록체인 검증 중 오류가 발생했습니다.\n\n{e}"
                )