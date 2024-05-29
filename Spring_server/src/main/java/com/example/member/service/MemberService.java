package com.example.member.service;

import com.example.member.dto.MemberDTO;
import com.example.member.entity.MemberEntity;
import com.example.member.repository.MemberRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.lang.reflect.Member;
import java.util.Optional;

@RequiredArgsConstructor
@Service
public class MemberService {
    private final MemberRepository memberRepository;
    public void save(MemberDTO memberDTO) {
        //repository의 save 메서드 호출 (조건 : entitiy 객체를 넘겨줘야함)
        //1. dto-> entity 변환
        //2. repository의 save메서드 호출
        MemberEntity memberEntity = MemberEntity.toMemberEntity(memberDTO);
        memberRepository.save(memberEntity); //jpa에서 자동으로해주는 save?



    }

    public MemberDTO login(MemberDTO memberDTO) {
        /*
        1. 회원이 입력한 학번으로 DB에서 조회를 함
        2. DB에서 조회한 비밀번호와 사용자가 입력한 비밀번호가 일치하는지 판단
        */
        Optional<MemberEntity> byMemberStudentId = memberRepository.findByMemberStudentId(memberDTO.getMemberStudentId());
        if(byMemberStudentId.isPresent()){
            //조회 결과가 있다(가입된 학번이 있다)
            MemberEntity memberEntity = byMemberStudentId.get();
            if(memberEntity.getMemberPassword().equals(memberDTO.getMemberPassword())) {
                //비밀번호 일치
                //entity -> dto 변환 후 리턴
                MemberDTO dto = MemberDTO.toMemberDTO(memberEntity);
                return dto;
            } else{
                //비밀번호 불일치(로그인실패)
                return null;
            }
        } else{
            //조회 결과가 없다(가입된 학번이 없다)
            return null;
        }
    }
}
