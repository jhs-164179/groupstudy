package com.example.member.dto;

import com.example.member.entity.MemberEntity;
import lombok.Getter; //필드에 대한 Getter를 자동으로 만들어줌
import lombok.NoArgsConstructor; //기본생성자를 만들어줌
import lombok.Setter; //Setter를 자동으로 만들어줌
import lombok.ToString; //ToString을 자동으로

@Getter
@Setter
@NoArgsConstructor
@ToString
public class MemberDTO { //필드를 정의?
    private Long id;
    private Long memberStudentId; //Long형식이므로 다른걸 입력하면 whitelabel error page가 떴었음
    private String memberName;
    private String memberPassword;

    public static MemberDTO toMemberDTO(MemberEntity memberEntity){
        MemberDTO memberDTO = new MemberDTO();
        memberDTO.setId(memberEntity.getId());
        memberDTO.setMemberStudentId(memberEntity.getMemberStudentId());
        memberDTO.setMemberPassword(memberEntity.getMemberPassword());
        memberDTO.setMemberName(memberEntity.getMemberName());
        return memberDTO;
    }
}
